const BASE_URL = "http://localhost:8000";

function authHeader(): Record<string, string> {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export interface AuthPayload {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  role: string;
}

export interface CargoRow {
  id: number;
  cargo_id: string;
  origin: string;
  destination: string;
  weight_kg: number;
}

export interface UploadResult {
  received: number;
  saved: number;
  skipped_prime: number;
  malformed: number;
}

async function asJson<T>(res: Response): Promise<T> {
  const body = (await res.json().catch(() => ({}))) as { detail?: string };
  if (!res.ok) {
    throw new Error(body.detail ?? `HTTP ${res.status}`);
  }
  return body as T;
}

export const api = {
  async signup(payload: AuthPayload) {
    const res = await fetch(`${BASE_URL}/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return asJson<{ id: number; email: string; role: string }>(res);
  },

  async login(payload: AuthPayload) {
    const res = await fetch(`${BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return asJson<AuthResponse>(res);
  },

  async listCargo() {
    const res = await fetch(`${BASE_URL}/api/cargo`, { headers: authHeader() });
    return asJson<CargoRow[]>(res);
  },

  async uploadManifest(file: File) {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${BASE_URL}/api/upload`, {
      method: "POST",
      headers: authHeader(),
      body: form,
    });
    return asJson<UploadResult>(res);
  },
};
