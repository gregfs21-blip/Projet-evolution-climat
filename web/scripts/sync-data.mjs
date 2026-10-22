// Copie data/processed (produit par l'ETL) dans web/.data avant le build.
// Le site ne lit que cette copie : il reste autonome dans son dossier, ce qui
// évite toute dépendance au traçage de fichiers hors projet sur Vercel.
import { cpSync, existsSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const webDir = join(dirname(fileURLToPath(import.meta.url)), "..");
const source = process.env.DATA_DIR ?? join(webDir, "..", "data", "processed");
const target = join(webDir, ".data");

if (!existsSync(join(source, "manifest.json"))) {
  console.error(`[sync-data] manifest.json introuvable dans ${source}. Lancer d'abord l'ETL.`);
  process.exit(1);
}
rmSync(target, { recursive: true, force: true });
cpSync(source, target, { recursive: true });
console.log(`[sync-data] ${source} → ${target}`);
