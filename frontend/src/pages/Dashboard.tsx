import { useCallback, useEffect, useState } from "react";
import { api, CargoRow, UploadResult } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { CargoTable } from "../components/CargoTable";
import { UploadButton } from "../components/UploadButton";

export default function Dashboard() {
  const { role, clearSession } = useAuth();
  const [rows, setRows] = useState<CargoRow[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastUpload, setLastUpload] = useState<UploadResult | null>(null);

  const refresh = useCallback(async () => {
    try {
      const cargo = await api.listCargo();
      setRows(cargo);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load cargo");
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return (
    <div className="app-shell">
      <div className="toolbar">
        <h1>Cargo Manifest</h1>
        <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
          <span className="role-pill">{role}</span>
          {/*
            PDF rule: the upload button MUST NOT exist in the DOM for Standard
            users. Conditional render (not `display:none`) keeps the element
            genuinely absent from the rendered tree for non-Admin sessions.
          */}
          {role === "Admin" && (
            <UploadButton
              onUploaded={(r) => {
                setLastUpload(r);
                void refresh();
              }}
            />
          )}
          <button onClick={clearSession}>Log out</button>
        </div>
      </div>
      <div className="card">
        {lastUpload && (
          <div className="success">
            Uploaded {lastUpload.received} rows — saved {lastUpload.saved}, skipped {lastUpload.skipped_prime} prime, {lastUpload.malformed} malformed.
          </div>
        )}
        {error && <div className="error">{error}</div>}
        {rows === null && !error ? (
          <p>Loading cargo...</p>
        ) : rows && rows.length === 0 ? (
          <p>No cargo records yet.</p>
        ) : rows && role ? (
          <CargoTable rows={rows} role={role} />
        ) : null}
      </div>
    </div>
  );
}
