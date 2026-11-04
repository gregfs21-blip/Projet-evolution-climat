import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Tout le site est pré-calculé au déploiement : aucune page n'est rendue à la demande.
  reactStrictMode: true,
  // Photo de l'accueil, servie par le site socio-vote du même compte.
  images: {
    remotePatterns: [{ protocol: "https", hostname: "correlation-socio-vote.vercel.app", pathname: "/accueil/**" }],
  },
};

export default nextConfig;
