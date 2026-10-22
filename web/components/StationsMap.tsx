"use client";

// Carte des stations : position et valeur d'un indicateur résumé (ex. pente 1962-2022).
// Fond OpenFreeMap (gratuit, sans clé, données OpenStreetMap).
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef } from "react";

export type MapPoint = { id: string; name: string; lat: number; lon: number; value: number | null; href: string };

const STYLE = "https://tiles.openfreemap.org/styles/positron";

export default function StationsMap({ points, legend }: { points: MapPoint[]; legend: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let map: import("maplibre-gl").Map | undefined;
    let disposed = false;
    (async () => {
      const { Map, Marker, NavigationControl } = await import("maplibre-gl");
      if (disposed || !ref.current || points.length === 0) return;
      const lats = points.map((p) => p.lat);
      const lons = points.map((p) => p.lon);
      map = new Map({
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
      const values = points.map((p) => p.value).filter((v): v is number => v !== null);
      const lo = Math.min(...values);
      const hi = Math.max(...values);
      for (const p of points) {
        const el = document.createElement("a");
        el.href = p.href;
        el.className = "station-marker";
        const k = p.value === null || hi === lo ? 0.5 : (p.value - lo) / (hi - lo);
        el.style.setProperty("--k", String(k));
        el.textContent = p.value === null ? "—" : p.value.toLocaleString("fr-FR", { signDisplay: "always", maximumFractionDigits: 2, minimumFractionDigits: 2 });
        el.title = `${p.name} : ${el.textContent} ${legend}`;
        new Marker({ element: el }).setLngLat([p.lon, p.lat]).addTo(map);
        const label = document.createElement("div");
        label.className = "station-label";
        label.textContent = p.name;
        new Marker({ element: label, anchor: "top", offset: [0, 14] }).setLngLat([p.lon, p.lat]).addTo(map);
      }
    })();
    return () => {
      disposed = true;
      map?.remove();
    };
  }, [points, legend]);

  return (
    <figure className="space-y-2">
      <div ref={ref} className="h-[420px] w-full overflow-hidden rounded-md border border-[var(--rule)]" />
      <figcaption className="text-xs text-[var(--muted)]">{legend}. Cliquer sur une valeur ouvre la station.</figcaption>
    </figure>
  );
}
