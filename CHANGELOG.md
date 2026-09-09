# Changelog

All notable updates to the FOMC Hawk-Dove Tracker are logged here. Add a new entry at the top each time you push a refreshed `index.html`.

Format: `## [Date] — Meeting/event covered`

---

## [2026-07-29] — Automated refresh via GitHub Actions

- Added `scripts/refresh_data.py` — calls the Claude API with web search to pull the latest FOMC data
- Added `.github/workflows/refresh.yml` — runs daily at 13:00 UTC, plus manual trigger from the Actions tab
- Added `data.json` — machine-readable data file, rewritten on each automated run and committed back to the repo
- `index.html` now fetches `data.json` on page load and renders it automatically; falls back to built-in static content if the file is unavailable
- Requires a one-time `ANTHROPIC_API_KEY` repo secret (see README)

## [2026-07-29] — July FOMC meeting (hawkish hold, 9–3)

- FOMC held at 3.50–3.75% for a 6th consecutive meeting
- **Three dissents** for an immediate 25bp hike: Hammack, Kashkari, Logan — first multi-dissent of Warsh's tenure
- Waller moved from Dovish → Neutral (signalled support for tighter policy if inflation persists)
- Overall sentiment score updated to 76/100 (most hawkish reading since the 2022 tightening cycle)
- Added metrics: Brent crude (~$88, down from $100+ mid-July on reported US–Iran pause), 30Y Treasury (5.19%, highest since 2007)
- Next meeting: Sept 15–16, ~75% hike odds priced
- Chart annotations added: "3 hawk dissents" (history chart), "Hawkish hold" (pricing chart)

## [2026-06-17] — June FOMC meeting (Warsh's first, unanimous 12–0 hold)

- Kevin Warsh's debut as Fed Chair (sworn in May 22, confirmed 54–45)
- Statement shortened from 341 to 130 words; forward guidance abandoned
- Easing bias language removed entirely — vindicating the three April hawkish dissenters
- Dot plot flipped from projecting a cut to projecting a hike (median 3.8% by year-end); Warsh declined to submit his own projection
- Added "The Warsh Regime Change" before/after comparison panel
- Miran voted with the majority for the first time in 2026 (previously dissented for cuts at every meeting)
- CPI 4.2% YoY, core PCE 3.4%, June payrolls +57k

## [2026-07-13] — Interim data refresh (pre-June-meeting placeholder — superseded)

- Initial build-out of leadership transition context ahead of the June 16–17 meeting
- Added Kevin Warsh confirmation details (54–45 Senate vote, sworn in May 22)
- Updated hike-odds framing as market repriced from cuts to hikes

## [2026-06-05] — Historical & market pricing charts extended to 2021

- Extended market pricing chart back to January 2021 (previously started 2023)
- Added effective fed funds rate as a right-axis overlay on the pricing chart
- Flipped pricing chart convention: hikes now plot above zero, cuts below zero
- Added event annotations: taper announcement (Nov 2021), first 75bp hike (Jun 2022)

## [2026-06-05] — Acheron Insights visual redesign

- Restyled entire dashboard to match the Acheron Insights editorial aesthetic
- Switched from dark theme to light theme: white background, warm off-white panels, hard edges
- Typography: Playfair Display (headings), Inter (body), DM Mono (data/metrics)
- Recoloured all three charts, tables, and badges for the new light palette

## [2026-06-05] — Historical data table added

- Added scrollable table (Jan 2000–present) mirroring the historical sentiment chart data
- Era filter buttons: Greenspan / Bernanke / Yellen / Powell / Warsh
- Key-event rows highlighted

## [2026-06-05] — Market pricing chart added

- New chart: number of 25bp cuts/hikes priced in by futures markets, 6- and 12-month horizons
- Initially covered Jan 2023–present (later extended back to 2021, see above)
- Annotated key repricing events: SVB collapse, Feb 2024 "7 cuts" peak, Sept 2024 first cut, Liberation Day tariff shock, Warsh confirmation

## [2026-06-05] — Historical sentiment chart added

- New chart: monthly hawk-dove sentiment score, January 2000–present, built from ~85 hand-curated milestone points with linear interpolation
- Effective fed funds rate overlaid on right axis
- Era dividers (chair tenures) and key-event annotations (9/11, Bear Stearns, Lehman, QE3, taper tantrum, COVID, CPI peak, 2024 pivot)

## [2026-06-05] — Initial dashboard build

- First version: current committee stance, hawk/dove member cards for all 12 voters, key metrics, policy outlook
- Covered the April 28–29, 2026 meeting (8–4 historic vote, 3 hawkish dissents against easing-bias language + 1 dovish dissent from Miran)
- Built as an interactive artifact with a "Refresh now" button calling the Anthropic API + web search for live updates
