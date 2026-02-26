"use client";

import { useState } from "react";

type OpenBackendLinkProps = {
  href: string;
  label: string;
  timeoutMs?: number;
};

export default function OpenBackendLink({ href, label, timeoutMs = 8000 }: OpenBackendLinkProps) {
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState("");

  async function handleClick() {
    setError("");
    setChecking(true);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    try {
      await fetch(href, {
        method: "HEAD",
        mode: "no-cors",
        cache: "no-store",
        signal: controller.signal,
      });
      window.open(href, "_blank", "noopener,noreferrer");
    } catch {
      setError("Backend haijibu kwa sasa. Jaribu tena baada ya sekunde chache.");
    } finally {
      clearTimeout(timer);
      setChecking(false);
    }
  }

  return (
    <div>
      <button type="button" onClick={handleClick} disabled={checking}>
        {checking ? "Opening..." : label}
      </button>
      {error ? <p className="error">{error}</p> : null}
    </div>
  );
}
