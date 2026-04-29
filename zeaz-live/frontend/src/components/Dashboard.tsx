import { useEffect, useState } from "react";

import { connectWS } from "../ws";
import Charts from "./Charts";
import DecisionFeed from "./DecisionFeed";

export default function Dashboard({ tenant }: any) {
  const [data, setData] = useState<any[]>([]);
  const [decision, setDecision] = useState("");

  useEffect(() => {
    const ws = connectWS(tenant, (d) => {
      setDecision(d.decision);
      setData((prev) => [...prev.slice(-30), { ...d.metrics, t: Date.now() }]);
    });
    return () => ws.close();
  }, [tenant]);

  return (
    <div>
      <h2>Tenant: {tenant}</h2>
      <h3>Decision: {decision}</h3>
      <DecisionFeed decision={decision} />
      <Charts data={data} />
    </div>
  );
}
