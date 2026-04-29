interface ExplainData {
  action?: string;
  reasons?: string[];
}

export default function ExplainPanel({ exp }: { exp?: ExplainData }) {
  return (
    <div style={{ border: "1px solid gray", padding: 10 }}>
      <h3>Decision Explanation</h3>
      <p>Action: {exp?.action}</p>
      <ul>
        {exp?.reasons?.map((reason, i) => (
          <li key={i}>{reason}</li>
        ))}
      </ul>
    </div>
  );
}
