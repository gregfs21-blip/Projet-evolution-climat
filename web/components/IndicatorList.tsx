import Link from "next/link";

import ConfidenceBadge from "./ConfidenceBadge";
import type { ManifestEntry } from "@/lib/schema";

export default function IndicatorList({ items }: { items: ManifestEntry[] }) {
  return (
    <ul className="divide-y divide-[var(--rule)] border-y border-[var(--rule)]">
      {items.map((e) => (
        <li key={`${e.scale}/${e.id}`}>
          <Link
            href={`/${e.scale}/${e.id}`}
            className="flex flex-col gap-1 py-3 hover:bg-[var(--hover)] sm:flex-row sm:items-center sm:justify-between sm:px-2"
          >
            <span>
              {e.title} <span className="text-[var(--muted)]">({e.unit})</span>
            </span>
            <ConfidenceBadge level={e.confidence} />
          </Link>
        </li>
      ))}
    </ul>
  );
}
