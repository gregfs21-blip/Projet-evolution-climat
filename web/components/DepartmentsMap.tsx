"use client";

// Carte des départements (P5 bis) : pente 1959-2021 de chaque département, pour la variable choisie.
// Couleurs sur l'échelle ABSOLUE du site (lib/heat.ts, ± 0,5 °C/déc.) ; pente non significative en teinte pâle ;
// département sans station : gris, sans valeur. Le site ne calcule rien : il colore les pentes publiées par l'ETL.
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useMemo, useRef, useState } from "react";

import HeatLegend from "./HeatLegend";
import Segmented from "./Segmented";
import type { DepartmentMap } from "@/lib/schema";
import { heatColor } from "@/lib/heat";

const STYLE = "https://tiles.openfreemap.org/styles/positron";
const NO_DATA = "#c9c9c9";
const fmt = (v: number) => v.toLocaleString("fr-FR", { signDisplay: "always", maximumFractionDigits: 2, minimumFractionDigits: 2 });

export default function DepartmentsMap({ data }: { data: DepartmentMap }) {
  const [variable, setVariable] = useState<string>(data.variables.find((v) => v.id === "tm")?.id ?? data.variables[0]!.id);
  const ref = useRef<HTMLDivElement>(null);
  const mapRef = useRef<import("maplibre-gl").Map | null>(null);
  const [ready, setReady] = useState(false);

  // Une entité par contour ; propriétés pré-calculées pour chaque variable (couleur, pente, significativité).
  const geojson = useMemo(() => {
    const byVar = Object.fromEntries(data.variables.map((v) => [v.id, new Map(v.departments.map((d) => [d.code, d]))]));
    return {
      type: "FeatureCollection" as const,
      features: data.shapes.map((s) => {
        const props: Record<string, string | number | boolean> = { code: s.code, name: s.name };
        for (const v of data.variables) {
          const d = byVar[v.id]!.get(s.value_code);
          props[`color_${v.id}`] = d ? heatColor(d.slope_per_decade, data.unit).bg : NO_DATA;
          props[`opacity_${v.id}`] = d ? (d.significant ? 0.88 : 0.38) : 0.55;
          props[`text_${v.id}`] = d
            ? `${fmt(d.slope_per_decade)} ${data.unit}/déc. · ${d.n_stations} station${d.n_stations > 1 ? "s" : ""}` +
              (d.significant ? "" : " · non significatif")
            : "aucune station au réseau";
        }
        return { type: "Feature" as const, properties: props, geometry: s.geometry };
      }),
    };
  }, [data]);

  useEffect(() => {
    let disposed = false;
    (async () => {
      const { Map, NavigationControl, Popup } = await import("maplibre-gl");
      if (disposed || !ref.current) return;
      const map = new Map({
        container: ref.current,
        style: STYLE,
        bounds: [
          [-5.2, 41.3],
          [9.6, 51.2],
        ],
        attributionControl: { compact: true },
        cooperativeGestures: true,
      });
      map.addControl(new NavigationControl({ showCompass: false }), "top-right");
      map.on("load", () => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        map.addSource("deps", { type: "geojson", data: geojson as any });
        map.addLayer({ id: "deps-fill", type: "fill", source: "deps", paint: { "fill-color": "#ccc", "fill-opacity": 0.5 } });
        map.addLayer({ id: "deps-line", type: "line", source: "deps", paint: { "line-color": "#ffffff", "line-width": 0.7 } });
        const popup = new Popup({ closeButton: false, closeOnClick: false });
        map.on("mousemove", "deps-fill", (e) => {
          const f = e.features?.[0];
          if (!f) return;
          map.getCanvas().style.cursor = "default";
          const v = (map.getContainer().dataset.variable ?? "tm") as string;
          popup
            .setLngLat(e.lngLat)
            .setHTML(`<strong>${f.properties.name}</strong><br/>${f.properties[`text_${v}`]}`)
            .addTo(map);
        });
        map.on("mouseleave", "deps-fill", () => popup.remove());
        mapRef.current = map;
        setReady(true);
      });
    })();
    return () => {
      disposed = true;
      mapRef.current?.remove();
      mapRef.current = null;
    };
  }, [geojson]);

  useEffect(() => {
    const map = mapRef.current;
    if (!ready || !map) return;
    map.getContainer().dataset.variable = variable;
    map.setPaintProperty("deps-fill", "fill-color", ["get", `color_${variable}`]);
    map.setPaintProperty("deps-fill", "fill-opacity", ["get", `opacity_${variable}`]);
  }, [ready, variable]);

  const current = data.variables.find((v) => v.id === variable)!;
  const nSig = current.departments.filter((d) => d.significant).length;
  return (
    <figure className="space-y-2">
      <div className="flex justify-end">
        <Segmented
          label="Variable"
          value={variable}
          onChange={setVariable}
          options={data.variables.map((v) => ({ key: v.id, label: v.code, title: v.label }))}
        />
      </div>
      <div ref={ref} className="h-[460px] w-full overflow-hidden rounded-md border border-[var(--rule)] sm:h-[560px]" />
      <figcaption className="space-y-2 text-xs text-[var(--muted)]">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <span>
            Tendance {current.code} {data.period.start}-{data.period.end}, en {data.unit} par décennie, par département ;
            France : {fmt(current.national_slope_per_decade)}. Pâle : non significatif ({current.departments.length - nSig}{" "}
            sur {current.departments.length}). Gris : aucune station au réseau.
          </span>
          <HeatLegend unit={data.unit} />
        </div>
        <p>{data.method_note}</p>
        <p>Contours : {data.geometry_source}.</p>
      </figcaption>
    </figure>
  );
}
