import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Tout le site est pré-calculé au déploiement : aucune page n'est rendue à la demande.
  reactStrictMode: true,
};

export default nextConfig;
