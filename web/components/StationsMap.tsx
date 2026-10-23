"use client";

// Carte des stations : pente de chaque station sur la période commune, pour la variable choisie.
// Couleurs sur l'échelle ABSOLUE de lib/heat.ts (identique à la matrice) : deux pentes voisines
// ont deux couleurs voisines, quelle que soit la dispersion des valeurs affichées.
// Fond OpenFreeMap (gratuit, sans clé, données OpenStreetMap).
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef, useState } from "react";

import HeatLegend from "./HeatLegend";
import Segmented from "./Segmented";
import type { MapPoint, VarKey } from "@/lib/family";
import { heatColor } from "@/lib/heat";

const STYLE = "https://tiles.openfreemap.org/styles/positron";
const CODES: Record<VarKey, string> = { tn: "TN", tm: "TM", tx: "TX" };
const fmt = (v: number) => v.toLocaleString("fr-FR", { signDisplay: "always", maximumFractionDigits: 2, minimumFractionDigits: 2 });

export default function StationsMap({
  points,
  variables,
  initial,
  period,
}: {
  points: Partial<Record<VarKey, MapPoint[]>>;
  variables: VarKey[];
  initial: VarKey;
  period: string;
}) {
  const [variable, setVariable] = useState<VarKey>(initial);
  const ref = useRef<HTMLDivElement>(null);
  const mapRef = useRef<import("maplibre-gl").Map | null>(null);
  const markersRef = useRef<import("maplibre-gl").Marker[]>([]);
  const [ready, setReady] = useState(false);

  // Carte créée une fois, cadrée sur l'ensemble des stations toutes variables confondues.
  useEffect(() => {
    let disposed = false;
    const all = Object.values(points).flat();
    (async () => {
      const { Map, NavigationControl } = await import("maplibre-gl");
      if (disposed || !ref.current || all.length === 0) return;
      const lats = all.map((p) => p.lat);
      const lons = all.map((p) => p.lon);
      const map = new Map({
        container: ref.current,
        style: STYLE,
        bounds: [
          [Math.min(...lons) - 0.25, Math.min(...lats) - 0.15],
          [Math.max(...lons) + 0.25, Math.max(...lats) + 0.15],
        ],
        attributionControl: { compact: true },
        cooperativeGestures: true,
      });
      map.addControl(new NavigationControl({ showCompass: false }), "top-right");
      mapRef.current = map;
      setReady(true);
    })();
    return () => {
      disposed = true;
      mapRef.current?.remove();
      mapRef.current = null;
    };
  }, [points]);

  // Marqueurs redessinés à chaque changement de variable.
  useEffect(() => {
    const map = mapRef.current;
    if (!ready || !map) return;
    let disposed = false;
    (async () => {
      const { Marker } = await import("maplibre-gl");
      if (disposed) return;
      markersRef.current.forEach((m) => m.remove());
      markersRef.current = [];
      for (const p of points[variable] ?? []) {
        const el = document.createElement("a");
        el.href = p.href;
        el.className = "station-marker";
        el.textContent = p.value === null ? "—" : fmt(p.value);
        if (p.value !== null) {
          const { bg, fg } = heatColor(p.value);
          el.style.background = bg;
          el.style.color = fg;
        }
        el.title = `${p.name} : ${el.textContent} °C par décennie (${CODES[variable]}, ${period})`;
        const label = document.createElement("div");
        label.className = "station-label";
        label.textContent = p.name;
        markersRef.current.push(
          new Marker({ element: el }).setLngLat([p.lon, p.lat]).addTo(map),
          new Marker({ element: label, anchor: "top", offset: [0, 14] }).setLngLat([p.lon, p.lat]).addTo(map),
        );
      }
    })();
    return () => {
      disposed = true;
    };
  }, [ready, variable, points, period]);

  return (
    <figure className="space-y-2">
      <div className="flex justify-end">
        <Segmented
          label="Variable"
          value={variable}
          onChange={setVariable}
          options={variables.map((v) => ({ key: v, label: CODES[v], disabled: !points[v]?.length }))}
        />
      </div>
      <div ref={ref} className="h-[340px] w-full overflow-hidden rounded-md border border-[var(--rule)] sm:h-[380px]" />
      <figcaption className="flex flex-wrap items-center justify-between gap-3 text-xs text-[var(--muted)]">
        <span>
          Tendance {CODES[variable]} {period}, en °C par décennie. Même échelle que la matrice. Une valeur ouvre la station.
        </span>
        <HeatLegend />
      </figcaption>
    </figure>
  );
}
