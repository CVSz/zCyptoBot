# ZCyptoBot Investor-Grade Pitch Package

This package includes a client-ready + investor-grade pitch deck narrative, full visual diagrams (SVG), branding guidance, financial model assumptions, valuation outputs, and a runnable demo with live metrics simulation.

## Contents
- `pitch_deck.md` — Full slide-by-slide investor narrative.
- `financial_model.csv` — 5-year operating model + valuation inputs.
- `diagrams/` — Architecture, GTM flywheel, and unit-economics SVG diagrams.
- `mockups/` — Grafana-style and SaaS dashboard mockups (HTML/CSS).
- `demo/` — Frontend + API + live metrics simulation.

## Run the demo
```bash
cd pitchdeck/demo
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```
Then open:
- API docs: `http://127.0.0.1:8000/docs`
- Dashboard: `http://127.0.0.1:8000/`
