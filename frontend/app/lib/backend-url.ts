const DEFAULT_BACKEND_URL = "https://burhan-2.onrender.com";

export function getBackendUrl(rawUrl?: string): string {
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

