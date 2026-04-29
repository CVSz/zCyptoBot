export async function getMetrics(tenant: string) {
  const response = await fetch(`http://localhost:8000/metrics/${tenant}`);
  return response.json();
}

export async function getDecision(tenant: string) {
  const response = await fetch(`http://localhost:8000/decision/${tenant}`);
  return response.json();
}
