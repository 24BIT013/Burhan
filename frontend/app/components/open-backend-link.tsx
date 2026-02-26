"use client";

import { useState } from "react";

type OpenBackendLinkProps = {
  href: string;
  label: string;
};

export default function OpenBackendLink({ href, label }: OpenBackendLinkProps) {
  const [notice, setNotice] = useState("");

  function handleClick() {
    setNotice("Ukiona loading ndefu, backend ya Render inaamka. Subiri sekunde 30-60.");
    window.open(href, "_blank", "noopener,noreferrer");
  }

  return (
    <div>
      <button type="button" onClick={handleClick}>
        {label}
      </button>
      {notice ? <p className="error">{notice}</p> : null}
    </div>
  );
}
