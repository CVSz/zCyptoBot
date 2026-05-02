export type Locale = "en" | "es";

export type Messages = Record<string, string>;

const fallbackMessages: Messages = {
  control_plane_title: "ZEAZ SaaS Control Plane",
  tab_dashboard: "Dashboard",
  tab_admin: "Admin",
  tab_billing: "Billing",
  tab_tenants: "Tenants",
};

export async function fetchMessages(locale: Locale): Promise<Messages> {
  const response = await fetch(`http://localhost:8000/i18n/messages?locale=${locale}`);
  if (!response.ok) return fallbackMessages;
  const payload = await response.json();
  return { ...fallbackMessages, ...(payload.messages ?? {}) };
}
