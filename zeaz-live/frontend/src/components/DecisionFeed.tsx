export default function DecisionFeed({ decision }: { decision: string }) {
  return <p>Latest decision: {decision || "waiting for stream..."}</p>;
}
