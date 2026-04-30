"use client";

import { useEffect, useState } from "react";

export default function Forecast() {
  const [f, setF] = useState<any>({});

  useEffect(() => {
    fetch("/api/forecast").then((r) => r.json()).then(setF);
  }, []);

  return (
    <div>
      <h1>Revenue Forecast</h1>
      <p>${f.forecast}</p>
    </div>
  );
}
