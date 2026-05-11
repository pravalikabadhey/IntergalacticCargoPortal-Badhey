import { AuthProvider } from "./auth/AuthContext";

export default function App() {
  return (
    <AuthProvider>
      <div className="app-shell">
        <div className="card">
          <h1>Intergalactic Cargo Portal</h1>
          <p>Routing and pages land in the next commit.</p>
        </div>
      </div>
    </AuthProvider>
  );
}
