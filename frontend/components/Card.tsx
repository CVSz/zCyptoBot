import type { ReactNode } from "react";

type CardProps = {
  children: ReactNode;
  title?: string;
};

export function Card({ children, title }: CardProps) {
  return (
    <section
      style={{
        background: "#0B0F1A",
        color: "#E6ECFF",
        padding: 16,
        borderRadius: 12,
        border: "1px solid rgba(123,97,255,0.35)",
        boxShadow: "0 0 20px rgba(123,97,255,0.3)",
      }}
    >
      {title && <h3 style={{ marginTop: 0 }}>{title}</h3>}
      {children}
    </section>
  );
}
