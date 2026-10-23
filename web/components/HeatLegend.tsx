// Légende de l'échelle de couleur absolue des tendances (lib/heat.ts). Rien si l'unité n'a pas d'échelle.
import { fmtSigned } from "@/lib/format";
import { heatGradient, heatMax } from "@/lib/heat";

export default function HeatLegend({ unit, className = "" }: { unit: string; className?: string }) {
  const max = heatMax(unit);
  if (max === null) return null;
  const ticks = [-max, -max / 2, 0, max / 2, max];
  return (
    <div className={`w-full max-w-64 ${className}`} aria-label={`Échelle de couleur fixe, de ${fmtSigned(-max)} à ${fmtSigned(max)} ${unit} par décennie`}>
      <div className="h-2.5 rounded-sm" style={{ background: heatGradient(unit) }} />
      <div className="mt-1 flex justify-between font-mono text-[10px] text-[var(--muted)]">
        {ticks.map((t) => (
          <span key={t}>{t === 0 ? "0" : fmtSigned(t)}</span>
        ))}
      </div>
    </div>
  );
}
