export default function Billing({ messages }: { messages: Record<string, string> }) {
  return (
    <div>
      <h2>{messages.billing_title || "Billing"}</h2>
      <p>{messages.billing_description || "Usage metering and invoice status (Stripe-ready skeleton)."}</p>
    </div>
  );
}
