"use client";

import { useEffect, useState } from "react";

export default function CRM() {
  const [data, setData] = useState<any>({});

  useEffect(() => {
    fetch("/api/pipeline").then((r) => r.json()).then(setData);
  }, []);

  return (
    <div>
      <h1>Sales Pipeline</h1>
      <p>Pipeline Value: ${data.value}</p>
    </div>
  );
}
