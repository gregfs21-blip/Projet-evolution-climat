"use client";

// Critère Q5 (P11) : si la page affichée date de plus de 30 minutes (source en panne, régénération refusée), le
// lecteur le voit. Calculé dans le navigateur, à l'heure du lecteur.
import { useEffect, useState } from "react";

import { staleMinutes } from "@/lib/metar";

export default function StaleBanner({ readAt }: { readAt: string }) {
  const [stale, setStale] = useState<number | null>(null);
  useEffect(() => {
    const tick = () => setStale(staleMinutes(readAt, new Date()));
    tick();
    const id = window.setInterval(tick, 60_000);
    return () => window.clearInterval(id);
  }, [readAt]);
  if (stale === null) return null;
  return (
    <p role="status" className="rounded-lg border border-[var(--warm)] px-4 py-2 text-sm">
      Ces valeurs datent de {stale} minutes : la source ne répond pas ou la page n&apos;a pas encore été régénérée.
      Rechargez dans quelques instants.
    </p>
  );
}
