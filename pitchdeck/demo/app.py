from __future__ import annotations

import asyncio
import math
import random
import time
from collections import defaultdict
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="Zypto Live AI Decision Engine Demo")

TENANTS = {
    "alpha-capital": {"plan": "Enterprise", "users": 84, "api_limit": 1_000_000},
    "nova-digital": {"plan": "Growth", "users": 26, "api_limit": 250_000},
    "retail-labs": {"plan": "Starter", "users": 8, "api_limit": 50_000},
}

connections: Dict[str, List[WebSocket]] = defaultdict(list)


def generate_signal(tenant_id: str) -> dict:
    now = int(time.time())
    phase = now / 14
    wave = math.sin(phase)
    confidence = max(0.5, min(0.99, 0.76 + wave * 0.18 + random.uniform(-0.08, 0.08)))
    action = random.choices(["BUY", "SELL", "HOLD"], weights=[0.4, 0.35, 0.25])[0]
    symbol = random.choice(["BTC-USD", "ETH-USD", "SOL-USD", "ARB-USD"])

    risk_score = max(0.01, min(0.95, 0.35 + random.uniform(-0.15, 0.2) + (1 - confidence) * 0.2))
    exec_latency = max(22.0, round(58 + random.uniform(-25, 18) + (1 - confidence) * 25, 2))
    fill_rate = max(92.5, min(99.99, round(98.7 - risk_score * 3 + random.uniform(-0.6, 0.7), 2)))

    pnl_delta = round(random.uniform(-1100, 1500) * confidence, 2)
    regime = random.choice(["Trend", "Mean-Revert", "Volatility Breakout", "Range"])

    return {
        "tenant_id": tenant_id,
        "timestamp": now,
        "signal": {
            "action": action,
            "symbol": symbol,
            "confidence": round(confidence, 3),
            "regime": regime,
            "reasoning": [
                f"Orderbook imbalance detected on {symbol}",
                f"{regime} regime confidence at {round(confidence * 100, 1)}%",
                "Cross-exchange spread favorable for smart routing",
            ],
        },
        "execution": {
            "latency_ms_p50": exec_latency,
            "fill_rate": fill_rate,
            "risk_score": round(risk_score, 3),
            "slippage_bps": round(max(0.4, 6.2 - confidence * 4 + random.uniform(-0.8, 1.2)), 2),
        },
        "business": {
            "pnl_delta": pnl_delta,
            "mrr_usd": round(random.uniform(35_000, 155_000), 2),
            "api_calls": random.randint(2000, 12000),
            "active_strategies": random.randint(4, 21),
        },
    }


@app.get("/api/tenants")
def tenants():
    return {"tenants": [{"tenant_id": k, **v} for k, v in TENANTS.items()]}


@app.get("/api/tenant/{tenant_id}/snapshot")
def tenant_snapshot(tenant_id: str):
    if tenant_id not in TENANTS:
        return {"error": "tenant not found"}
    return generate_signal(tenant_id)


@app.websocket("/ws/{tenant_id}")
async def ws_tenant_stream(websocket: WebSocket, tenant_id: str):
    await websocket.accept()
    if tenant_id not in TENANTS:
        await websocket.send_json({"error": "tenant not found"})
        await websocket.close()
        return

    connections[tenant_id].append(websocket)
    try:
        while True:
            await websocket.send_json(generate_signal(tenant_id))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in connections[tenant_id]:
            connections[tenant_id].remove(websocket)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!doctype html>
<html>
<head>
  <meta charset='utf-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1' />
  <title>Zypto Live AI Decision Engine</title>
  <script crossorigin src='https://unpkg.com/react@18/umd/react.development.js'></script>
  <script crossorigin src='https://unpkg.com/react-dom@18/umd/react-dom.development.js'></script>
  <script src='https://unpkg.com/@babel/standalone/babel.min.js'></script>
  <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
  <style>
    body{margin:0;font-family:Inter,Arial,sans-serif;background:#020617;color:#e2e8f0}
    .wrap{padding:18px 24px}
    .top{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap}
    .title{font-size:24px;font-weight:700}.muted{color:#94a3b8}
    .grid{display:grid;gap:12px;margin-top:14px;grid-template-columns:repeat(4,minmax(180px,1fr))}
    .card{background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:12px}
    .k{color:#94a3b8;font-size:12px;text-transform:uppercase}.v{font-size:28px;font-weight:700;color:#22d3ee}
    .layout{display:grid;grid-template-columns:2fr 1fr;gap:12px;margin-top:12px}
    .table{width:100%;border-collapse:collapse}.table td,.table th{padding:8px;border-bottom:1px solid #1e293b;text-align:left}
    .pill{padding:4px 8px;border-radius:999px;background:#1e293b;display:inline-block}
    select{background:#0f172a;color:#e2e8f0;border:1px solid #334155;padding:8px;border-radius:8px}
    @media(max-width:1000px){.grid{grid-template-columns:repeat(2,minmax(170px,1fr))}.layout{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <div id='root'></div>
  <script type='text/babel'>
    const {useEffect, useMemo, useRef, useState} = React;

    function App(){
      const [tenant, setTenant] = useState('alpha-capital');
      const [tenantMeta, setTenantMeta] = useState([]);
      const [feed, setFeed] = useState([]);
      const [latest, setLatest] = useState(null);
      const pnlRef = useRef(null);
      const riskRef = useRef(null);
      const charts = useRef({});

      useEffect(()=>{ fetch('/api/tenants').then(r=>r.json()).then(d=>setTenantMeta(d.tenants || [])); },[]);

      useEffect(()=>{
        setFeed([]); setLatest(null);
        const ws = new WebSocket(`${location.protocol==='https:'?'wss':'ws'}://${location.host}/ws/${tenant}`);
        ws.onmessage = (ev)=>{
          const d = JSON.parse(ev.data);
          if(d.error) return;
          setLatest(d);
          setFeed(prev=>[...prev.slice(-59), d]);
        };
        return ()=>ws.close();
      },[tenant]);

      useEffect(()=>{
        if(!pnlRef.current || !riskRef.current) return;
        if(!charts.current.pnl){
          charts.current.pnl = new Chart(pnlRef.current, {type:'line', data:{labels:[], datasets:[{label:'PnL Δ', data:[], borderColor:'#22d3ee'}]}});
          charts.current.risk = new Chart(riskRef.current, {type:'line', data:{labels:[], datasets:[{label:'Risk Score', data:[], borderColor:'#f43f5e'}]}});
        }
        const labels = feed.map(x=>new Date(x.timestamp*1000).toLocaleTimeString());
        charts.current.pnl.data.labels = labels;
        charts.current.pnl.data.datasets[0].data = feed.map(x=>x.business.pnl_delta);
        charts.current.pnl.update('none');

        charts.current.risk.data.labels = labels;
        charts.current.risk.data.datasets[0].data = feed.map(x=>x.execution.risk_score);
        charts.current.risk.update('none');
      },[feed]);

      const m = latest || {signal:{},execution:{},business:{}};
      const chosen = useMemo(()=>tenantMeta.find(t=>t.tenant_id===tenant),[tenantMeta, tenant]);

      return <div className='wrap'>
        <div className='top'>
          <div>
            <div className='title'>Zypto • Live AI Decision Engine</div>
            <div className='muted'>Realtime signal generation, execution telemetry, and SaaS multi-tenant controls.</div>
          </div>
          <div><span className='muted'>Tenant:</span> <select value={tenant} onChange={e=>setTenant(e.target.value)}>{tenantMeta.map(t=><option key={t.tenant_id} value={t.tenant_id}>{t.tenant_id}</option>)}</select></div>
        </div>

        <div className='grid'>
          <div className='card'><div className='k'>Action</div><div className='v'>{m.signal.action || '--'}</div><div>{m.signal.symbol || ''}</div></div>
          <div className='card'><div className='k'>Confidence</div><div className='v'>{m.signal.confidence ? `${(m.signal.confidence*100).toFixed(1)}%` : '--'}</div><div>{m.signal.regime || ''}</div></div>
          <div className='card'><div className='k'>Latency P50</div><div className='v'>{m.execution.latency_ms_p50 || '--'} ms</div><div>Fill {m.execution.fill_rate || '--'}%</div></div>
          <div className='card'><div className='k'>Risk Score</div><div className='v'>{m.execution.risk_score || '--'}</div><div>Slippage {m.execution.slippage_bps || '--'} bps</div></div>
        </div>

        <div className='layout'>
          <div className='card'>
            <h3>Realtime Decision & Risk Streams</h3>
            <canvas ref={pnlRef} height='110'></canvas>
            <canvas ref={riskRef} height='110' style={{marginTop:'10px'}}></canvas>
          </div>
          <div className='card'>
            <h3>SaaS Tenant Panel</h3>
            <p><span className='muted'>Plan:</span> <span className='pill'>{chosen?.plan || '--'}</span></p>
            <p><span className='muted'>Users:</span> {chosen?.users || '--'}</p>
            <p><span className='muted'>API Limit:</span> {(chosen?.api_limit || 0).toLocaleString()}</p>
            <p><span className='muted'>Active Strategies:</span> {m.business.active_strategies || '--'}</p>
            <p><span className='muted'>MRR:</span> ${m.business.mrr_usd || '--'}</p>
          </div>
        </div>

        <div className='card' style={{marginTop:'12px'}}>
          <h3>AI Rationale Feed</h3>
          <table className='table'><thead><tr><th>Time</th><th>Action</th><th>Confidence</th><th>Reasoning</th></tr></thead><tbody>
            {feed.slice().reverse().slice(0,10).map((x,idx)=><tr key={idx}><td>{new Date(x.timestamp*1000).toLocaleTimeString()}</td><td>{x.signal.action} {x.signal.symbol}</td><td>{(x.signal.confidence*100).toFixed(1)}%</td><td>{x.signal.reasoning[0]}</td></tr>)}
          </tbody></table>
        </div>
      </div>
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
  </script>
</body>
</html>
"""
