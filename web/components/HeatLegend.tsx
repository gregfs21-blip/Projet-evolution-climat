// Légende de l'échelle de couleur absolue des tendances (lib/heat.ts).
import { HEAT_MAX, heatGradient } from "@/lib/heat";
import { fmtSigned } from "@/lib/format";

export default function HeatLegend({ className = "" }: { className?: string }) {
  const ticks = [-HEAT_MAX, -HEAT_MAX / 2, 0, HEAT_MAX / 2, HEAT_MAX];
  return (
    <div className={`w-full max-w-64 ${className}`} aria-label={`Échelle de couleur fixe, de ${fmtSigned(-HEAT_MAX)} à ${fmtSigned(HEAT_MAX)} °C par décennie`}>
      <div className="h-2.5 rounded-sm" style={{ background: heatGradient() }} />
      <div className="mt-1 flex justify-between font-mono text-[10px] text-[var(--muted)]">
        {ticks.map((t) => (
          <span key={t}>{t === 0 ? "0" : fmtSigned(t)}</span>
        ))}
      </div>
    </div>
  );
}
