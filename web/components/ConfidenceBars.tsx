// Répartition des séries publiées par niveau de confiance et par échelle, comptée sur le manifeste.
// Séquence d'une seule teinte (du plus au moins établi) ; « non établi » hachuré, car ce n'est pas un degré de plus mais une absence de conclusion.
import Link from "next/link";

import { CONFIDENCE_LABELS } from "@/lib/format";
import { CONFIDENCE_ORDER, confidenceByScale } from "@/lib/home";
import type { Confidence } from "@/lib/schema";

const FILL: Record<Confidence, React.CSSProperties> = {
  elevee: { background: "var(--primary)" },
  moyenne: { background: "color-mix(in srgb, var(--primary) 55%, var(--card))" },
  faible: { background: "color-mix(in srgb, var(--primary) 25%, var(--card))" },
  non_etabli: { background: "repeating-linear-gradient(45deg, var(--muted) 0 1.5px, var(--hover) 1.5px 5px)" },
};

export default function ConfidenceBars() {
  const rows = confidenceByScale();
  const total = rows.reduce((a, r) => a + r.total, 0);
  return (
    <div className="space-y-4">
      <div className="space-y-3">
        {rows.map((r) => (
          <div key={r.scale} className="space-y-1">
            <div className="flex items-baseline justify-between text-sm">
              <Link href={`/${r.scale}`} className="font-medium underline-offset-2 hover:underline">
                {r.name}
              </Link>
              <span className="text-xs tabular-nums text-[var(--muted)]">{r.total} séries</span>
            </div>
            <div className="flex h-5 gap-0.5 overflow-hidden rounded">
              {r.counts
                .filter((c) => c.n > 0)
                .map((c) => (
                  <div key={c.level} style={{ ...FILL[c.level], flexGrow: c.n, flexBasis: 0 }} title={`${CONFIDENCE_LABELS[c.level]} : ${c.n}`} />
                ))}
            </div>
            <p className="text-xs tabular-nums text-[var(--muted)]">
              {r.counts.filter((c) => c.n > 0).map((c, i) => `${i ? ", " : ""}${c.n} ${CONFIDENCE_LABELS[c.level].replace("Confiance ", "").replace("Signal ", "")}`)}
            </p>
          </div>
        ))}
      </div>
      <ul className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-[var(--muted)]">
        {CONFIDENCE_ORDER.map((l) => (
          <li key={l} className="inline-flex items-center gap-1.5">
            <i className="inline-block h-2.5 w-3.5 rounded-sm" style={FILL[l]} />
            {CONFIDENCE_LABELS[l]}
          </li>
        ))}
      </ul>
      <p className="text-xs text-[var(--muted)]">
        {total} séries, stations comprises : la Gironde en compte davantage parce qu&apos;elle détaille chaque station. Ce sont des séries, pas des conclusions
        indépendantes.
      </p>
    </div>
  );
}
