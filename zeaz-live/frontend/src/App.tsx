import { useState } from "react";

import Dashboard from "./components/Dashboard";
import TenantSelector from "./components/TenantSelector";

export default function App() {
  const [tenant, setTenant] = useState("t1");

  return (
    <div>
      <h1>ZEAZ Control Panel</h1>
      <TenantSelector setTenant={setTenant} />
      <Dashboard tenant={tenant} />
    </div>
  );
}
