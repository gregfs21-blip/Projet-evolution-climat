import Link from "next/link";

export default function NotFound() {
  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Page introuvable</h1>
      <p className="text-[var(--muted)]">Cet indicateur ou cette échelle n&apos;existe pas.</p>
      <Link href="/" className="underline underline-offset-2">
        Retour à l&apos;accueil
      </Link>
    </div>
  );
}
