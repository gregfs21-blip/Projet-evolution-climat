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
    <div role="radiogroup" aria-label={label} className="inline-flex flex-wrap gap-0.5 rounded-full bg-[var(--hover)] p-0.5 text-sm">
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
            className={`rounded-full px-3 py-1 ${
              on ? "bg-[var(--primary)] font-medium text-[var(--primary-ink)]" : "text-[var(--muted)] hover:text-[var(--ink)]"
            } disabled:cursor-not-allowed disabled:opacity-40`}
          >
            {o.label}
          </button>
        );
      })}
    </div>
  );
}
