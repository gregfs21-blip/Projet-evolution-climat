import { CONFIDENCE_LABELS } from "@/lib/format";
import type { Confidence } from "@/lib/schema";

const TONE: Record<Confidence, string> = {
  elevee: "border-[var(--good)] text-[var(--good)]",
  moyenne: "border-[var(--accent)] text-[var(--accent)]",
  faible: "border-[var(--warm)] text-[var(--warm)]",
  non_etabli: "border-[var(--muted)] text-[var(--muted)]",
};

export default function ConfidenceBadge({ level }: { level: Confidence }) {
  return (
    <span className={`inline-block rounded-full border px-2.5 py-0.5 text-xs font-medium ${TONE[level]}`}>
      {CONFIDENCE_LABELS[level]}
    </span>
  );
}
