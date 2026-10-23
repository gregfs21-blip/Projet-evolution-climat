"use client";

// Sélecteur à boutons segmentés (TN / TM / TX, anomalie / valeur absolue…).
export type SegOption<K extends string> = { key: K; label: string; disabled?: boolean; title?: string };

export default function Segmented<K extends string>({
  options,
  value,
  onChange,
  label,
}: {
  options: SegOption<K>[];
  value: K;
  onChange: (k: K) => void;
  label: string;
}) {
  return (
    <div role="radiogroup" aria-label={label} className="inline-flex overflow-hidden rounded-md border border-[var(--rule)] text-sm">
      {options.map((o) => {
        const on = o.key === value;
        return (
          <button
            key={o.key}
            type="button"
            role="radio"
            aria-checked={on}
            disabled={o.disabled}
            title={o.title}
            onClick={() => onChange(o.key)}
            className={`px-3 py-1 ${
              on ? "bg-[var(--ink)] text-[var(--paper)]" : "text-[var(--muted)] hover:bg-[var(--hover)]"
            } disabled:cursor-not-allowed disabled:opacity-40`}
          >
            {o.label}
          </button>
        );
      })}
    </div>
  );
}
