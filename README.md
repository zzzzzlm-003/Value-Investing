# greenwald-av-epv-valuation-tool

Python / Streamlit tool for **Bruce Greenwald-style** equity valuation:

- **AV** — Asset Value  
- **EPV** — Earnings Power Value  
- **FV** — Franchise Value (growth / competitive advantage)

Not a course archive. Use this when you want to run the valuation app or reuse the `valuation/` package on a ticker.

## Quick start

```bash
cd greenwald-av-epv-valuation-tool
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # if present
./run.sh                          # or: streamlit run dashboard/...
```

Company research notes and filings live in **`equity-research/companies/`**, not here.

Site (if deployed): https://zzzzzlm-003.github.io/Value-Investing/  
(GitHub repo renamed to match this folder; Pages URL may still use the old name until updated.)
