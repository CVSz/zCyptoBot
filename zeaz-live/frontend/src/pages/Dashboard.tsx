import { useEffect, useState } from "react";

type LiveData = {
  state?: { latency?: number; error?: number; load?: number };
  action?: string;
  cost?: number;
  usage_total?: number;
};

export default function Dashboard() {
  const [data, setData] = useState<LiveData>({});

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/t1");
    ws.onmessage = (e) => setData(JSON.parse(e.data));
    return () => ws.close();
  }, []);

  return (
    <div>
      <h2>ZEAZ SaaS Dashboard</h2>
      <p>Latency: {data.state?.latency?.toFixed(2)}</p>
      <p>Error: {data.state?.error?.toFixed(4)}</p>
      <p>Action: {data.action}</p>
      <p>Cost (tick): {data.cost?.toFixed(4)}</p>
      <p>Total usage: {data.usage_total?.toFixed(4)}</p>
    </div>
  );
}
