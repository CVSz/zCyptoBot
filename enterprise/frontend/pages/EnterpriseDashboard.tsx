"use client";
import { useEffect, useState } from "react";

export default function EnterpriseDashboard() {
  const [data, setData] = useState<any>({});

  useEffect(() => {
    fetch("/api/dashboard")
      .then((r) => r.json())
      .then(setData);
  }, []);

  return (
    <div style={{ padding: 30 }}>
      <h1>Enterprise ROI Dashboard</h1>

      <div>Original Cost: ${data.original_cost}</div>
      <div>ZEAZ Cost: ${data.zeaz_cost}</div>
      <div>Savings: ${data.savings}</div>
      <div>ROI: {(data.roi * 100)?.toFixed(2)}%</div>
      <div>Margin: ${data.margin}</div>
    </div>
  );
}
