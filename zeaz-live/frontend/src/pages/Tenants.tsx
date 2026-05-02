export default function Tenants({ messages }: { messages: Record<string, string> }) {
  return (
    <div>
      <h2>{messages.tenants_title || "Tenants"}</h2>
      <p>{messages.tenants_description || "Multi-tenant management and access overview."}</p>
    </div>
  );
}
