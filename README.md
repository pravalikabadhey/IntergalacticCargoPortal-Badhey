# IntergalacticCargoPortal — Badhey

Full-stack portal with Authentication and Role-Based Access Control (RBAC) for legacy cargo manifests.

**Stack:** Python (FastAPI) · SQLite · React (Vite + TypeScript) · JWT auth

## Repository layout

```
.
├── backend/                  FastAPI app + SQLite + manifest parser
│   ├── app/
│   │   ├── auth.py          bcrypt hashing + JWT issue/verify
│   │   ├── config.py        JWT secret + expiry
│   │   ├── db.py            SQLAlchemy engine / session
│   │   ├── main.py          FastAPI app, CORS, route registration
│   │   ├── models.py        User, Cargo
│   │   ├── parser.py        manifest parser + business rules
│   │   ├── rbac.py          require_role("Admin") with 403 message
│   │   ├── routes/auth.py   /signup, /login
│   │   ├── routes/cargo.py  GET /api/cargo, POST /api/upload
│   │   └── schemas.py       Pydantic models
│   ├── tests/test_rules.py  pytest for Sector-7 + prime rules + parser
│   └── requirements.txt
└── frontend/                 Vite + React + TypeScript SPA
    ├── src/api/client.ts    fetch wrapper with JWT auto-attach
    ├── src/auth/            AuthContext + ProtectedRoute
    ├── src/pages/           Login, Signup, Dashboard
    ├── src/components/      CargoTable, UploadButton
    └── src/styles.css
```

Each PDF task was developed in its own git worktree on a feature branch (`task-1-foundation`, `task-2-core-engine`, `task-3-frontend`) and merged into `main` on completion.

## Prerequisites

- **Python 3.12** (3.13 works but the original passlib version had issues — we use direct `bcrypt` now)
- **Node.js 20+** with npm 10+
- That's it — SQLite is bundled with Python

## Backend setup

```bash
cd backend

# create + activate a venv
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

# launch the API on port 8000 (CORS allows http://localhost:5173)
uvicorn app.main:app --reload --port 8000
```

The first request creates `cargo.db` (SQLite) in the `backend/` directory.

### Creating an Admin user

Role assignment is enforced by the backend, not the client. Sign up with an email ending **exactly** in `@nebula-corp.com` and the user is provisioned as `Admin`; everything else gets `Standard`.

```bash
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"founder@nebula-corp.com","password":"secret123"}'
# → {"id": 1, "email": "founder@nebula-corp.com", "role": "Admin"}
```

### Sample `manifest.txt`

Pipe-delimited with an optional header row:

```
ID|ORIGIN|DESTINATION|WEIGHT
C1|Mars|Sector-7|100
C2|Mars|Sector-7|4
C3|Jupiter|Mars|8
C4|Jupiter|Mars|2
C5|Saturn|Earth|9999
C6|Pluto|Sector-7-Outpost|10
C7|Mars|Sector-7|2
```

Upload as Admin:

```bash
curl -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer <admin-jwt>" \
  -F "file=@manifest.txt"
# → {"received":7,"saved":5,"skipped_prime":2,"malformed":0}
```

Business rules applied (see `backend/app/parser.py`):
- Destinations **containing** `Sector-7` have their weight multiplied by **1.45**.
- The result is rounded to the nearest whole number (round-half-up).
- If the rounded weight is **prime**, the row is **dropped**.

### Running the backend tests

```bash
cd backend
pytest -q
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev    # http://localhost:5173
```

The dashboard calls the backend at `http://localhost:8000` (see `frontend/src/api/client.ts`). Make sure the backend is running first.

### What each role sees

| Role     | Upload button     | Weight column        |
|----------|-------------------|----------------------|
| Admin    | rendered          | `<N> KG`             |
| Standard | **absent in DOM** | `<N * 2.20462> LBS`  |

Sort order is heaviest → lightest, with **any cargo destined for `Earth` pinned to the absolute bottom** regardless of weight.

### Production build

```bash
cd frontend
npm run build
npm run preview
```

## Reset the database

```bash
rm backend/cargo.db
# next API call recreates the schema
```
