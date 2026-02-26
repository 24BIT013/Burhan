const DEFAULT_BACKEND_URL = "https://burhan-2.onrender.com";

function normalizeBackendUrl(rawUrl) {
  const trimmed = (rawUrl || "").trim();
  if (!trimmed) return DEFAULT_BACKEND_URL;

  const withScheme = /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`;

  try {
    const parsed = new URL(withScheme);
    parsed.pathname = "";
    parsed.search = "";
    parsed.hash = "";
    return parsed.toString().replace(/\/$/, "");
  } catch {
    return DEFAULT_BACKEND_URL;
  }
}

/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    const backendUrl = normalizeBackendUrl(process.env.NEXT_PUBLIC_BACKEND_URL);
    return [
      {
        source: "/backend/:path*",
        destination: `${backendUrl}/:path*`
      }
    ];
  }
};

export default nextConfig;

