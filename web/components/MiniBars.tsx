// Mini-courbe (SVG rendu au build, sans JavaScript) : barres, droite de Sen, années brutes en gris.
// Anomalie : rouge au-dessus de zéro, bleu en dessous. Comptage (pas d'anomalie) : barres neutres, le signe n'a pas de sens.
type Props = {
  time: string[];
  value: (number | null)[];
  quality: ("homogenized" | "raw")[] | null;
  trend: { start: number; end: number; fittedStart: number; fittedEnd: number } | null;
  isAnomaly?: boolean;
};

const W = 300;
const H = 64;

export default function MiniBars({ time, value, quality, trend, isAnomaly = true }: Props) {
  const years = time.map((t) => Number(t.slice(0, 4)));
  const vals = value.filter((v): v is number => v !== null);
  if (years.length === 0 || vals.length === 0) return null;
  const x0 = years[0]!;
  const n = years[years.length - 1]! - x0 + 1;
  const lo = Math.min(0, ...vals);
  const hi = Math.max(0, ...vals);
  const X = (y: number) => ((y - x0) / n) * W;
  const Y = (v: number) => 2 + ((hi - v) / (hi - lo || 1)) * (H - 4);
  const bw = (W / n) * 0.75;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" className="h-16 w-full" aria-hidden>
      <line x1={0} x2={W} y1={Y(0)} y2={Y(0)} style={{ stroke: "var(--rule)" }} strokeWidth={1} />
      {years.map((y, i) => {
        const v = value[i];
        if (v === null || v === undefined) return null;
        const [a, b] = [Y(0), Y(v)].sort((p, q) => p - q) as [number, number];
        const fill = quality?.[i] === "raw" ? "var(--muted)" : !isAnomaly ? "var(--accent)" : v >= 0 ? "var(--warm)" : "var(--cold)";
        return <rect key={y} x={X(y)} y={a} width={bw} height={Math.max(0.8, b - a)} style={{ fill, opacity: quality?.[i] === "raw" ? 0.45 : 0.9 }} />;
      })}
      {trend && (
        <line
          x1={X(trend.start)}
          y1={Y(trend.fittedStart)}
          x2={X(trend.end) + bw}
          y2={Y(trend.fittedEnd)}
          style={{ stroke: "var(--ink)" }}
          strokeWidth={1.6}
          strokeDasharray="5 3"
          vectorEffect="non-scaling-stroke"
        />
      )}
    </svg>
  );
}
