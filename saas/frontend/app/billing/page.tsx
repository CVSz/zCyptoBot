"use client";

export default function BillingPage() {
  const subscribe = async () => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000"}/create-checkout`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plan: "pro" }),
    });
    const payload = await response.json();
    if (payload.url) window.location.href = payload.url;
  };

  return (
    <main style={{ padding: 24, fontFamily: "Inter, sans-serif" }}>
      <h1>Billing</h1>
      <p>Upgrade to Pro to unlock full realtime analytics.</p>
      <button onClick={subscribe}>Subscribe with Stripe</button>
    </main>
  );
}
