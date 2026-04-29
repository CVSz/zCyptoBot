"use client";

import { useEffect, useMemo, useState } from "react";

type MetricsFrame = {
  ts: string;
  latency: number;
  revenue: number;
  active_users: number;
};

function Sparkline({ values, color }: { values: number[]; color: string }) {
  const points = useMemo(() => {
    if (!values.length) return "";
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = Math.max(1, max - min);
    return values
      .map((v, i) => `${(i / Math.max(1, values.length - 1)) * 100},${100 - ((v - min) / range) * 100}`)
      .join(" ");
  }, [values]);

  return (
    <svg viewBox="0 0 100 100" style={{ width: "100%", height: 56 }}>
      <polyline fill="none" stroke={color} strokeWidth="3" points={points} />
    </svg>
  );
}

export default function Dashboard() {
  const [frames, setFrames] = useState<MetricsFrame[]>([]);

  useEffect(() => {
    const ws = new WebSocket(process.env.NEXT_PUBLIC_METRICS_WS ?? "ws://localhost:8000/ws/metrics");
    ws.onmessage = (event) => {
      const next = JSON.parse(event.data) as MetricsFrame;
      setFrames((prev) => [...prev.slice(-39), next]);
    };
    return () => ws.close();
  }, []);

  const latest = frames[frames.length - 1];

  return (
    <main style={{ maxWidth: 1040, margin: "0 auto", padding: 24, fontFamily: "Inter, sans-serif" }}>
      <h1 style={{ fontSize: 28, marginBottom: 20 }}>ZEAZ Live Metrics</h1>
      <section style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
        <article style={{ background: "#0b1220", color: "white", borderRadius: 12, padding: 16 }}>
          <h3>Latency (ms)</h3>
          <p style={{ fontSize: 22 }}>{latest?.latency ?? "--"}</p>
          <Sparkline values={frames.map((f) => f.latency)} color="#60a5fa" />
        </article>
        <article style={{ background: "#081b12", color: "white", borderRadius: 12, padding: 16 }}>
          <h3>Revenue ($)</h3>
          <p style={{ fontSize: 22 }}>{latest?.revenue ?? "--"}</p>
          <Sparkline values={frames.map((f) => f.revenue)} color="#34d399" />
        </article>
        <article style={{ background: "#1f1403", color: "white", borderRadius: 12, padding: 16 }}>
          <h3>Active users</h3>
          <p style={{ fontSize: 22 }}>{latest?.active_users ?? "--"}</p>
          <Sparkline values={frames.map((f) => f.active_users)} color="#fbbf24" />
        </article>
      </section>
    </main>
  );
}
