# Task 2 — Core Engine (Uploads)

This branch (`task-2-core-engine`) builds on Task 1 by adding the `Cargo` table, the protected `POST /api/upload` and `GET /api/cargo` endpoints, and the manifest parser implementing the Sector-7 multiplier and prime-skip business rules.

## Run

All commands run from the **worktree root**. `--app-dir backend` lets uvicorn find the `app/` package without changing directory.

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1            # or: source .venv/bin/activate
pip install -r backend/requirements.txt
pip install pytest                    # for the unit tests
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

## What to test

### 1. Unit tests (parser + business rules)

Run from the worktree root (pytest needs to find the `app` package, hence the `cd`):

```bash
cd backend && pytest -q
# expected: 24 passed
```

Coverage includes `is_prime` (incl. 0/1 NOT prime), Sector-7 substring match, prime-only-after-multiplier skip, round-half-up rounding, malformed-row counting, header-row tolerance, blank-line tolerance.

### 2. RBAC — Standard cannot upload (Authorisation Rule)

```bash
# Sign up a Standard user (non-nebula email)
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" \
  -d '{"email":"crew@example.com","password":"pw"}'

STD=$(curl -s -X POST http://localhost:8000/login -H "Content-Type: application/json" \
  -d '{"email":"crew@example.com","password":"pw"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

curl -i -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer $STD" \
  -F "file=@../sample_manifest.txt"
# HTTP/1.1 403 Forbidden
# {"detail":"Clearance level inadequate."}
```

The 403 body is byte-exact — note the capital `C`, lower-case rest, and the trailing period.

### 3. Live business rules — Admin upload

```bash
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" \
  -d '{"email":"admin@nebula-corp.com","password":"pw"}'

ADMIN=$(curl -s -X POST http://localhost:8000/login -H "Content-Type: application/json" \
  -d '{"email":"admin@nebula-corp.com","password":"pw"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

curl -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer $ADMIN" \
  -F "file=@../sample_manifest.txt"
# → {"received":7,"saved":5,"skipped_prime":2,"malformed":0}
```

Expected row-by-row evaluation of `sample_manifest.txt`:

| ID | Destination       | Input | ×1.45 | Rounded | Prime? | Saved as |
|----|-------------------|------:|------:|--------:|:------:|---------:|
| C1 | Sector-7          | 100   | 145.0 | 145     | no     | **145**  |
| C2 | Sector-7          | 4     | 5.8   | 6       | no     | **6**    |
| C3 | Mars              | 8     | —     | 8       | no     | **8**    |
| C4 | Mars              | 2     | —     | 2       | **yes**| dropped  |
| C5 | Earth             | 9999  | —     | 9999    | no     | **9999** |
| C6 | Sector-7-Outpost  | 10    | 14.5  | 15      | no     | **15**   |
| C7 | Sector-7          | 2     | 2.9   | 3       | **yes**| dropped  |

C6 confirms the "contains `Sector-7`" rule (substring, not exact). C7 confirms primality is checked **after** the multiplier and rounding.

### 4. List cargo

```bash
curl -H "Authorization: Bearer $ADMIN" http://localhost:8000/api/cargo
# Standard users can also read this endpoint:
curl -H "Authorization: Bearer $STD"   http://localhost:8000/api/cargo
```

Unauthenticated → `401`.

## Submission email

- Subject: `Update: Task 2 - Badhey - DB Populated`
- Body: the exact cURL command from section **2** above (the 403 attempt).
- Screenshot name: `Task 2 - Screenshot 1 - Badhey - Error`
