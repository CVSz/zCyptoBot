export default function TenantSelector({ setTenant }: any) {
  return (
    <select onChange={(e) => setTenant(e.target.value)}>
      <option value="t1">Tenant 1</option>
      <option value="t2">Tenant 2</option>
    </select>
  );
}
