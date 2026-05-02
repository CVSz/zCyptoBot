import { useEffect, useState } from "react";

import Admin from "./pages/Admin";
import Billing from "./pages/Billing";
import Dashboard from "./pages/Dashboard";
import Tenants from "./pages/Tenants";
import { fetchMessages, Locale, Messages } from "./i18n";

const tabs = ["dashboard", "admin", "billing", "tenants"] as const;
type Tab = (typeof tabs)[number];

export default function App() {
  const [tab, setTab] = useState<Tab>("dashboard");
  const [locale, setLocale] = useState<Locale>("en");
  const [messages, setMessages] = useState<Messages>({});

  useEffect(() => {
    fetchMessages(locale).then(setMessages);
  }, [locale]);

  const labelMap: Record<Tab, string> = {
    dashboard: messages.tab_dashboard || "Dashboard",
    admin: messages.tab_admin || "Admin",
    billing: messages.tab_billing || "Billing",
    tenants: messages.tab_tenants || "Tenants",
  };

  return (
    <div>
      <h1>{messages.control_plane_title || "ZEAZ SaaS Control Plane"}</h1>
      <label>
        Language:
        <select value={locale} onChange={(e) => setLocale(e.target.value as Locale)}>
          <option value="en">English</option>
          <option value="es">Español</option>
        </select>
      </label>
      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
        {tabs.map((t) => (
          <button key={t} onClick={() => setTab(t)}>
            {labelMap[t]}
          </button>
        ))}
      </div>
      {tab === "dashboard" && <Dashboard locale={locale} messages={messages} />}
      {tab === "admin" && <Admin messages={messages} />}
      {tab === "billing" && <Billing messages={messages} />}
      {tab === "tenants" && <Tenants messages={messages} />}
    </div>
  );
}
