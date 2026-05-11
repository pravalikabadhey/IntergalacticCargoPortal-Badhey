# Task 1 — Foundation (Auth & DB)

This branch (`task-1-foundation`) delivers the FastAPI server, SQLite schema, and `/signup` + `/login` endpoints with JWT auth and email-based role provisioning.

## Run

All commands here are run from the **worktree root** (this directory). `--app-dir backend` tells uvicorn where the `app/` package lives, so you don't have to `cd` first.

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1            # PowerShell, or: source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

The `users` table is created on first start in `/Users/pravalikabadhey/Desktop/Evaluation_proj_Pravuu/common_database/cargo.db`.

## What to test

### 1. Role provisioning (Business Rule 1)

Email ending **exactly** in `@nebula-corp.com` → `Admin`. Everything else → `Standard`. The client cannot select the role.

```bash
# Admin
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" \
  -d '{"email":"founder@nebula-corp.com","password":"abcd"}'
# → {"id":1,"email":"founder@nebula-corp.com","role":"Admin"}

# Standard
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"pqrs"}'
# → {"id":2,"email":"alice@example.com","role":"Standard"}

# Role spoof in payload — silently dropped, still Standard
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" \
  -d '{"email":"sneaky@example.com","password":"x","role":"Admin"}'
# → {"id":3,"email":"sneaky@example.com","role":"Standard"}
```

Endswith-not-substring edge cases (both must be `Standard`):

```bash
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" \
  -d '{"email":"bad@nebula-corp.com.evil.com","password":"x"}'
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" \
  -d '{"email":"alice@sub.nebula-corp.com","password":"x"}'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/login -H "Content-Type: application/json" \
  -d '{"email":"founder@nebula-corp.com","password":"secret123"}'
# → {"access_token":"<jwt>","token_type":"bearer","role":"Admin"}
```

Wrong password → `401`. Duplicate signup → `409`.

### 3. Schema

For the Task 1 submission screenshot, inspect `/Users/pravalikabadhey/Desktop/Evaluation_proj_Pravuu/common_database/cargo.db` in DB Browser for SQLite. Expected schema:

```
users
├── id             INTEGER  PRIMARY KEY AUTOINCREMENT
├── email          VARCHAR  NOT NULL  UNIQUE  (indexed)
├── password_hash  VARCHAR  NOT NULL
└── role           VARCHAR  NOT NULL   -- "Admin" | "Standard"
```

## Submission email

- Subject: `Update: Task 1 - Badhey - Auth Ready`
- Body JSON payload: `{"email":"founder@nebula-corp.com","password":"secret123"}`
- Screenshot name: `Task 1 - Screenshot 1 - Badhey - Auth Ready`
