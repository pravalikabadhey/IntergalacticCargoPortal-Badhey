import { useAuth } from "../auth/AuthContext";

export default function Dashboard() {
  const { role, clearSession } = useAuth();
  return (
    <div className="app-shell">
      <div className="toolbar">
        <h1>Cargo Manifest</h1>
        <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
          <span className="role-pill">{role}</span>
          <button onClick={clearSession}>Log out</button>
        </div>
      </div>
      <div className="card">
        <p>Cargo table lands in the next commit.</p>
      </div>
    </div>
  );
}
