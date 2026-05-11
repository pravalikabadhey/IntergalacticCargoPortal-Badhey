import { ChangeEvent, useRef, useState } from "react";
import { api, UploadResult } from "../api/client";

interface Props {
  onUploaded(result: UploadResult): void;
}

export function UploadButton({ onUploaded }: Props) {
  const ref = useRef<HTMLInputElement | null>(null);
  const [busy, setBusy] = useState(false);

  async function pick(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setBusy(true);
    try {
      const result = await api.uploadManifest(file);
      onUploaded(result);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setBusy(false);
      if (ref.current) ref.current.value = "";
    }
  }

  return (
    <>
      <button type="button" onClick={() => ref.current?.click()} disabled={busy}>
        {busy ? "Uploading..." : "Upload manifest"}
      </button>
      <input
        ref={ref}
        type="file"
        accept=".txt"
        style={{ display: "none" }}
        onChange={pick}
      />
    </>
  );
}
