import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from "react";

export type Role = "Admin" | "Standard";

interface AuthState {
  token: string | null;
  role: Role | null;
}

interface AuthContextValue extends AuthState {
  setSession(token: string, role: Role): void;
  clearSession(): void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const STORAGE_KEY = "icp.auth";

function loadInitial(): AuthState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { token: null, role: null };
    const parsed = JSON.parse(raw) as { token?: string; role?: string };
    if (parsed.token && (parsed.role === "Admin" || parsed.role === "Standard")) {
      return { token: parsed.token, role: parsed.role };
    }
  } catch {
    /* ignore */
  }
  return { token: null, role: null };
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>(loadInitial);

  useEffect(() => {
    if (state.token && state.role) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      localStorage.setItem("token", state.token);
    } else {
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem("token");
    }
  }, [state]);

  const value = useMemo<AuthContextValue>(
    () => ({
      token: state.token,
      role: state.role,
      setSession: (token, role) => setState({ token, role }),
      clearSession: () => setState({ token: null, role: null }),
    }),
    [state]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
