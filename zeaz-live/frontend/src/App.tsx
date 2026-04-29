import { useState } from "react";

import Admin from "./pages/Admin";
import Billing from "./pages/Billing";
import Dashboard from "./pages/Dashboard";
import Tenants from "./pages/Tenants";

const tabs = ["dashboard", "admin", "billing", "tenants"] as const;
type Tab = (typeof tabs)[number];

export default function App() {
  const [tab, setTab] = useState<Tab>("dashboard");

  return (
    <div>
      <h1>ZEAZ SaaS Control Plane</h1>
      <div style={{ display: "flex", gap: 8 }}>
        {tabs.map((t) => (
          <button key={t} onClick={() => setTab(t)}>
            {t}
          </button>
        ))}
      </div>
      {tab === "dashboard" && <Dashboard />}
      {tab === "admin" && <Admin />}
      {tab === "billing" && <Billing />}
      {tab === "tenants" && <Tenants />}
    </div>
  );
}
