import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Tout le site est pré-calculé au déploiement, sauf /instantane (P11, décision D-AJ), régénérée par Vercel au plus
  // toutes les 10 minutes à partir des METAR de la NOAA.
  reactStrictMode: true,
};

export default nextConfig;
