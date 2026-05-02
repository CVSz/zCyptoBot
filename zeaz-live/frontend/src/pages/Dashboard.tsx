import { useEffect, useState } from "react";

type LiveData = {
  state?: { latency?: number; error?: number; load?: number };
  action?: string;
  cost?: number;
  usage_total?: number;
};

export default function Dashboard({ locale, messages }: { locale: string; messages: Record<string, string> }) {
  const [data, setData] = useState<LiveData>({});

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/t1?locale=${locale}`);
    ws.onmessage = (e) => setData(JSON.parse(e.data));
    return () => ws.close();
  }, [locale]);

  return (
    <div>
      <h2>{messages.dashboard_title || "ZEAZ SaaS Dashboard"}</h2>
      <p>{messages.latency || "Latency"}: {data.state?.latency?.toFixed(2)}</p>
      <p>{messages.error || "Error"}: {data.state?.error?.toFixed(4)}</p>
      <p>{messages.action || "Action"}: {data.action}</p>
      <p>{messages.cost_tick || "Cost (tick)"}: {data.cost?.toFixed(4)}</p>
      <p>{messages.total_usage || "Total usage"}: {data.usage_total?.toFixed(4)}</p>
    </div>
  );
}
