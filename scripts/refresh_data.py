#!/usr/bin/env python3
"""
Refreshes data.json with the latest FOMC data by calling the Claude API
with web search enabled. Run manually with:

    ANTHROPIC_API_KEY=sk-ant-... python scripts/refresh_data.py

In GitHub Actions, ANTHROPIC_API_KEY is injected from the repo secret
of the same name (see .github/workflows/refresh.yml).
"""

import json
import os
import sys
import re
from datetime import datetime, timezone

import anthropic

SYSTEM_PROMPT = """You are a Federal Reserve analyst. Search the web for the most \
current FOMC data then output ONLY valid JSON (no markdown fences) matching this \
exact schema:
{
  "updated": "ISO date",
  "rate_range": "e.g. 3.50-3.75%",
  "last_meeting": "e.g. July 28-29, 2026",
  "next_meeting": "e.g. September 15-16, 2026",
  "vote_result": "e.g. 9-3 (hawkish hold)",
  "overall_stance": "Decidedly Hawkish|Leaning Hawkish|Neutral|Leaning Dovish|Decidedly Dovish",
  "overall_stance_score": 0-100,
  "stance_summary": "2-3 sentences",
  "policy_outlook": "2-4 sentences",
  "hawk_count": number,
  "neutral_count": number,
  "dove_count": number,
  "alert": null_or_string,
  "members": [{
    "name": "Full name",
    "title": "Role",
    "voter": true/false,
    "stance": "Hawkish|Neutral|Dovish",
    "stance_score": 0-100,
    "dissent": null_or_"hawkish"_or_"dovish",
    "dissent_detail": null_or_"brief detail",
    "is_new": false,
    "note": "2-3 sentence current view with recent quotes",
    "latest_source": "most recent speech/event"
  }]
}

Search strategy:
1. Latest FOMC statement and minutes
2. Fed Chair's most recent public remarks / press conference
3. Each of the 12 current voting members individually: Kevin Warsh, Jerome Powell,
   John Williams, Michael Barr, Michelle Bowman, Lisa Cook, Philip Jefferson,
   Christopher Waller, Stephen Miran, Beth Hammack, Neel Kashkari, Lorie Logan,
   Anna Paulson
4. Current CPI, unemployment, and Fed funds futures pricing (CME FedWatch)

Output ONLY the JSON object. No preamble, no markdown code fences, no commentary."""

USER_PROMPT_TEMPLATE = """Today is {today}. Search for:
1. The most recent FOMC meeting statement and minutes
2. The Fed Chair's latest public remarks
3. Individual recent speeches/votes from all 12 current FOMC voters listed in your
   instructions
4. Current CPI, unemployment, and Fed funds futures pricing

Output ONLY the JSON described in your system prompt."""


# Current Sonnet-tier model ID. If a run fails with a 404 / NotFoundError,
# the model has likely been retired — check the current IDs at
# https://platform.claude.com/docs/en/about-claude/models/overview
MODEL = "claude-sonnet-5"


def call_model(client, today_str):
    return client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(today=today_str)}
        ],
    )


def extract_json(text: str) -> dict:
    cleaned = re.sub(r"```json\s*|\s*```", "", text).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model response")
    return json.loads(cleaned[start : end + 1])


def main() -> int:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        return 1

    client = anthropic.Anthropic(api_key=api_key)
    today_str = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")

    print(f"Requesting FOMC data refresh as of {today_str} using model {MODEL}...")

    try:
        response = call_model(client, today_str)
    except anthropic.NotFoundError as e:
        print(
            f"ERROR: Model '{MODEL}' was not found (it may have been retired).\n"
            "Check https://platform.claude.com/docs/en/about-claude/models/overview "
            "for current model IDs and update the MODEL constant at the top of this file.",
            file=sys.stderr,
        )
        print(f"Raw error: {e}", file=sys.stderr)
        return 1
    except anthropic.AuthenticationError:
        print(
            "ERROR: Authentication failed. Check that the ANTHROPIC_API_KEY repo secret "
            "is set correctly (Settings -> Secrets and variables -> Actions).",
            file=sys.stderr,
        )
        return 1
    except anthropic.APIStatusError as e:
        print(f"ERROR: API returned an error: {e}", file=sys.stderr)
        return 1

    # Web search shows up as server_tool_use blocks; count either form.
    search_calls = [
        b for b in response.content if b.type in ("tool_use", "server_tool_use")
    ]
    print(f"Model ran {len(search_calls)} web searches.")

    # Only take text blocks (skips any thinking / tool-result blocks).
    text_blocks = [b.text for b in response.content if b.type == "text"]
    full_text = "\n".join(text_blocks)

    if not full_text.strip():
        print("ERROR: No text content returned from the model.", file=sys.stderr)
        return 1

    try:
        data = extract_json(full_text)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: Failed to parse JSON from model output: {e}", file=sys.stderr)
        print("--- Raw model output ---", file=sys.stderr)
        print(full_text, file=sys.stderr)
        return 1

    # Stamp our own refresh time regardless of what the model returned,
    # so downstream consumers always have a reliable timestamp.
    data["updated"] = datetime.now(timezone.utc).isoformat()
    data["updated_by"] = "github-actions-scheduled-refresh"

    out_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    out_path = os.path.abspath(out_path)

    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"Wrote {len(data.get('members', []))} members to {out_path}")
    print(f"Rate range: {data.get('rate_range')} | Vote: {data.get('vote_result')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
