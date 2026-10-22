// Normales climatiques absolues et leur écart : le chiffre le plus parlant pour une station.
import { fmt, fmtSigned } from "@/lib/format";
import type { Indicator } from "@/lib/schema";

export default function Normals({ normals, unit }: { normals: Indicator["normals"]; unit: string }) {
  if (normals.length === 0) return null;
  const first = normals[0]!;
  const last = normals[normals.length - 1]!;
  return (
    <dl className="flex flex-wrap gap-x-10 gap-y-3">
      {normals.map((n) => (
        <div key={n.period.start}>
          <dt className="text-xs uppercase tracking-wide text-[var(--muted)]">
            Normale {n.period.start}–{n.period.end}
          </dt>
          <dd className="font-mono text-xl tabular-nums">
            {fmt(n.value)} {unit}
          </dd>
        </div>
      ))}
      {normals.length > 1 && (
        <div>
          <dt className="text-xs uppercase tracking-wide text-[var(--muted)]">Écart entre normales</dt>
          <dd className="font-mono text-xl tabular-nums">
            {fmtSigned(last.value - first.value)} {unit}
          </dd>
        </div>
      )}
    </dl>
  );
}
