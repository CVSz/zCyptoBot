export default function Admin({ messages }: { messages: Record<string, string> }) {
  return (
    <div>
      <h2>{messages.admin_title || "Admin Panel"}</h2>
      <p>{messages.admin_description || "Manage tenants, roles, policies, and model rollouts."}</p>
    </div>
  );
}
