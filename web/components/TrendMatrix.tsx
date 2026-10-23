// Matrice lieux × variables : pente sur la période commune, couleur sur l'échelle absolue.
// Remplace les listes de stations : toute la famille se compare d'un coup d'œil.
import Link from "next/link";

import HeatLegend from "./HeatLegend";
import { VARIABLES, type Matrix } from "@/lib/family";
import { fmtSigned } from "@/lib/format";
import { heatColor } from "@/lib/heat";

export default function TrendMatrix({ matrix }: { matrix: Matrix }) {
  const { variables, rows, period } = matrix;
  if (rows.length === 0) return null;
  return (
    <div className="space-y-3">
      <p className="text-xs text-[var(--muted)]">
        °C par décennie{period ? `, ${period.start}-${period.end}, période commune à toutes les stations` : ""}. Une case
        ouvre la série.
      </p>
      <div className="overflow-x-auto">
        <table className="w-full border-separate border-spacing-1 text-sm">
          <thead>
            <tr>
              <th className="sr-only">Lieu</th>
              {variables.map((v) => (
                <th key={v} className="px-1 text-center text-xs font-medium text-[var(--muted)]">
                  {VARIABLES[v].code} · {VARIABLES[v].short}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.place}>
                <th scope="row" className={`whitespace-nowrap pr-2 text-left ${r.isComposite ? "font-semibold" : "font-normal"}`}>
                  {r.name}
                </th>
                {variables.map((v) => {
                  const c = r.cells[v];
                  if (!c) {
                    return (
                      <td key={v} className="hatch rounded-md py-2 text-center text-[11px] text-[var(--muted)]">
                        pas de série
                      </td>
                    );
                  }
                  const { bg, fg } = heatColor(c.slope);
                  const ci = c.low !== null && c.high !== null ? ` (IC 95 % ${fmtSigned(c.low)} à ${fmtSigned(c.high)})` : "";
                  return (
                    <td key={v} className="p-0">
                      <Link
                        href={c.href}
                        title={`${r.name}, ${VARIABLES[v].code} : ${fmtSigned(c.slope)} °C/déc.${ci}`}
                        className={`block rounded-md py-2 text-center font-mono tabular-nums hover:brightness-110 ${r.isComposite ? "ring-2 ring-[var(--ink)] ring-inset" : ""}`}
                        style={{ background: bg, color: fg }}
                      >
                        {fmtSigned(c.slope)}
                      </Link>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex flex-wrap items-center gap-3">
        <span className="text-xs text-[var(--muted)]">Échelle fixe, °C/déc.</span>
        <HeatLegend className="flex-1" />
      </div>
    </div>
  );
}
