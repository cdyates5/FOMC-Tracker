# FOMC Hawk-Dove Tracker

A self-contained, single-file dashboard tracking the Federal Reserve's FOMC — committee-wide sentiment, individual voting member stances, market-implied rate pricing, and historical context back to 2000.

**Live site:** `https://yourusername.github.io/fomc-tracker/` *(update this line once Pages is enabled)*

---

## What's in the dashboard

- **Current committee stance** — overall hawk/dove reading with a spectrum needle, hawk/neutral/dove vote counts, and a plain-English summary
- **The Warsh regime change panel** — side-by-side comparison of Fed communication style before and after the June 2026 leadership change
- **Key metrics row** — fed funds rate, last/next meeting, CPI, unemployment, hike odds, and other headline figures
- **Member cards** — all 12 current voting FOMC members (Board of Governors, NY Fed, rotating regional presidents) with individual stance, recent votes/dissents, and sourcing
- **Historical sentiment chart** — monthly hawk-dove score from January 2000 to present, with the effective fed funds rate overlaid, annotated with major events (9/11, GFC, QE, taper tantrum, COVID, 2022 hiking cycle, etc.)
- **Historical data table** — the same dataset in tabular form, filterable by Fed chair era (Greenspan / Bernanke / Yellen / Powell / Warsh)
- **Market pricing chart** — number of 25bp cuts/hikes priced in by futures markets over 6- and 12-month horizons, from January 2021 to present, with the effective fed funds rate on the right axis
- **↻ Refresh now button** — calls the Anthropic API with web search to pull the latest FOMC statements, minutes, and member speeches (see note below on hosting)

---

## Hosting on GitHub Pages

1. Push this repo to GitHub (public repo required for free Pages)
2. Go to **Settings → Pages**
3. Source: **Deploy from a branch** → Branch: **main** → folder: **/ (root)** → Save
4. Your dashboard is live at `https://yourusername.github.io/<repo-name>/` within about a minute

## Repo structure

```
.
├── index.html                     # the dashboard (fetches data.json on load)
├── data.json                      # live data — rewritten by the scheduled Action
├── requirements.txt               # python deps for the refresh script
├── scripts/
│   └── refresh_data.py            # calls Claude API + web search, writes data.json
├── .github/workflows/
│   └── refresh.yml                # daily schedule + manual trigger
├── README.md
├── CHANGELOG.md
└── .gitignore
```

Only `data.json` changes on an automated run. `index.html` stays put unless you
change the layout, charts, or styling — those are structural edits you make by
hand (or by asking Claude for a new build).

---

## ⚙️ Automatic refresh (GitHub Actions)

This repo includes a scheduled **GitHub Action** that keeps the dashboard current without any manual work:

- **`.github/workflows/refresh.yml`** runs every day at 13:00 UTC (and can also be triggered manually from the repo's **Actions** tab)
- It runs **`scripts/refresh_data.py`**, which calls the Claude API with web search enabled to pull the latest FOMC statement, minutes, member speeches, and market data
- The script writes the result to **`data.json`**
- If `data.json` changed, the workflow commits it back to the repo automatically
- `index.html` fetches `data.json` on every page load and renders it — so the live site always reflects the most recent automated refresh, with zero manual steps

### One-time setup required

You need to give the workflow an Anthropic API key so it can call the API on your behalf:

1. Get an API key from [console.anthropic.com](https://console.anthropic.com/) (Settings → API Keys)
2. In your GitHub repo, go to **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Name: `ANTHROPIC_API_KEY`
5. Value: paste your key → **Add secret**

That's it — the next scheduled run (or your first manual trigger from the **Actions** tab) will use it. The key is encrypted by GitHub, never appears in logs, and is never exposed to site visitors, since it only runs server-side inside the Action.

### Running or checking it manually

- **Trigger a refresh right now:** go to the **Actions** tab → **Refresh FOMC data** (left sidebar) → **Run workflow** button
- **Check if it's working:** the Actions tab shows a green checkmark for each successful run, or a red X with logs if something failed (most common cause: missing/incorrect `ANTHROPIC_API_KEY` secret, or a temporary API/search error)
- **Change the schedule:** edit the `cron` line in `.github/workflows/refresh.yml`. The current setting (`0 13 * * *`) runs once daily; you could reduce it around FOMC meeting weeks or increase it if you want same-day updates after a press conference. [crontab.guru](https://crontab.guru/) is a handy tool for editing the schedule string.

### The manual "Refresh now" button

The button on the dashboard itself calls the Anthropic API directly from the browser. This **only works inside Claude's own chat/artifact environment**, which supplies credentials automatically — it will not work on the public GitHub Pages site, since there's no key available client-side (and embedding one in public HTML would expose it to anyone viewing the page source). This is expected and by design: the scheduled Action is the supported way to keep the public site updated automatically.

---

## Design

Visual style is intentionally matched to the [Acheron Insights](https://acheroninsights.substack.com/) editorial aesthetic — Playfair Display headings, Inter body copy, DM Mono for data/metrics, warm off-white panels on a white background, hard-edged borders, and a deep crimson/forest-green/navy palette for hawkish/dovish/neutral signal.

## Data & methodology notes

- The historical hawk-dove sentiment score (2000–present) is a **manually curated estimate**, not a quantitative formula — based on rate-change direction/pace, committee rhetoric, dissent patterns, and known pivot events, linearly interpolated between hand-set monthly anchor points. See the dashboard's in-chat conversation history for the full methodology discussion.
- Market pricing data (cuts/hikes priced in) is estimated from CME FedWatch, Bloomberg, and market commentary rather than pulled from a live data feed.
- All data is accurate as of the "Last updated" timestamp shown in the dashboard header — always check that timestamp before citing a figure.

## License

Personal/internal use. No warranty on data accuracy — this is a research and editorial tool, not investment advice.
