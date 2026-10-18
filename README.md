# Strength Desk

An NSE relative-strength (RS) dashboard and screener, built on real end-of-day prices.

- **RS Dashboard**: market breadth, sector and industry RS rankings, a filterable table of every rated stock, and an RS line chart with blue dots and an RS Rating history (TradingView-style indicator settings included).
- **Screener**: advancers/decliners, 52-week highs and lows, volume shockers, upper/lower circuit hits and sector movers.

## How it works

The site is static: `scripts/public/index.html` reads two data files from `scripts/public/data/`. `scripts/` is the folder Vercel deploys; `scripts/app.py` (and the root `app.py`) only exist so the site also works under Vercel's Python preset. The data pipeline lives in `pipeline/`.

| File | Contents |
|---|---|
| `scripts/public/data/rs.json` | RS ratings, returns and signals for ~2,400 NSE stocks, sector/industry aggregates, breadth, and 4 years of weekly prices for the charts |
| `scripts/public/data/screener.json` | The latest session's movers, circuits and sector changes |

A GitHub Action (`.github/workflows/update-data.yml`) rebuilds both files every weekday at 20:00 IST:

1. Downloads NSE daily prices (split/bonus adjusted) from [eod2_data](https://github.com/BennyThadikaran/eod2_data).
2. Runs `pipeline/compute_rs.py`, `pipeline/compute_screener.py` and `pipeline/embed.py`.
3. Commits the new data. Vercel redeploys on the commit.

Run it by hand from the **Actions** tab with **Run workflow**.

## RS Rating

Percentile rank (1–99) of `(2×C/C63 + C/C126 + C/C189 + C/C252) / 5` across every rated NSE stock. The latest quarter counts 40%. The chart settings can switch to an "own history" percentile, which ranks the stock against its own past scores the way a TradingView indicator does.

## Known limits

- Circuit hits are inferred from prices (closed at the day's high/low with a 2/5/10/20% move). NSE's EOD files don't include price bands.
- Result calendar and corporate actions need an announcements feed, which isn't connected.
- BSE-only stocks aren't included.

## Run locally

```bash
cd scripts/public && python3 -m http.server 8000   # then open http://localhost:8000
```
