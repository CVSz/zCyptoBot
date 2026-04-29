from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random, time

app = FastAPI(title="ZCyptoBot Live Demo")

@app.get("/metrics")
def metrics():
    base = int(time.time())
    return {
        "timestamp": base,
        "pnl_24h": round(random.uniform(12000, 58000), 2),
        "latency_ms_p50": round(random.uniform(65, 110), 2),
        "fill_rate": round(random.uniform(96.4, 99.7), 2),
        "error_rate": round(random.uniform(0.01, 0.15), 3),
    }

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!doctype html><html><head><meta charset='utf-8'><title>ZCyptoBot Demo</title>
<style>body{font-family:Arial;background:#0b1220;color:#e2e8f0;padding:24px}.kpi{display:flex;gap:16px}.card{background:#111827;border:1px solid #334155;border-radius:12px;padding:16px;min-width:220px}.v{font-size:30px;color:#22c55e}</style>
</head><body><h1>ZCyptoBot Live Metrics</h1><div class='kpi'><div class='card'><div>PnL (24h)</div><div id='pnl' class='v'>--</div></div><div class='card'><div>Latency P50</div><div id='lat' class='v'>--</div></div><div class='card'><div>Fill Rate</div><div id='fill' class='v'>--</div></div></div>
<script>async function tick(){const r=await fetch('/metrics');const d=await r.json();pnl.textContent='$'+d.pnl_24h;lat.textContent=d.latency_ms_p50+' ms';fill.textContent=d.fill_rate+'%';}setInterval(tick,1200);tick();</script>
</body></html>"""
