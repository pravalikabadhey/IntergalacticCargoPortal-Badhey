# Task 3 — Frontend Dashboard

This branch (`task-3-frontend`) adds the Vite + React + TypeScript SPA with a Login/Signup screen and a role-aware Dashboard. It includes the full backend from Tasks 1–2 so the whole portal runs end-to-end from this worktree.

## Run both servers

Two terminals — backend first, then frontend.

**Terminal 1 — backend (port 8000), run from the worktree root:**

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1            # or: source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

**Terminal 2 — frontend (port 5173):**

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The Vite dev server proxies nothing — the SPA calls the API directly at `http://localhost:8000` (CORS is whitelisted for `localhost:5173`).

## Browser test plan

### 1. Sign up two users

From the Sign-up screen create:
- `founderabcd@nebula-corp.com` / any password → backend provisions as **Admin**
- `crewabcd@example.com` / any password → backend provisions as **Standard**

After each signup the SPA auto-logs you in and routes to `/dashboard`. Log out between accounts via the **Log out** button.

### 2. Admin view (Business Rule 2 — KG)

Log in as `founderabcd@nebula-corp.com`. The dashboard should show:

- A **role pill** reading `Admin`
- An **Upload manifest** button
- Weights in the table formatted as `<N> KG`

Click **Upload manifest** and choose `../worktrees/task-2-core-engine/sample_manifest.txt` (or any pipe-delimited file). The success line should read:

> Uploaded 7 rows — saved 5, skipped 2 prime, 0 malformed.

### 3. Standard view (Business Rule 2 — LBS; upload absent from DOM)

Log out and back in as `crewabcd@example.com`. Verify:

- The role pill reads `Standard`.
- The **Upload manifest** button is **not** anywhere on the page.
- Weight column is now formatted as `<N> LBS` and values are KG × 2.20462.

**Prove the button is not in the DOM** (this is the PDF's exact rule):

1. Open DevTools → Elements.
2. `Ctrl+F` in the Elements panel, search for `Upload manifest`.
3. Zero matches — the element is conditionally not rendered, not merely hidden.

Or in the Console:

```js
[...document.querySelectorAll('button')].filter(b => /Upload manifest/.test(b.textContent))
// → []  (empty array)
```

### 4. Earth pin (Business Rule 3)

In both roles the table is sorted heaviest → lightest, **except** every row whose `destination` is `Earth` is pinned to the bottom regardless of weight. Using the seed manifest you uploaded:

| Position | Cargo | Weight (KG) | Why |
|---------:|------|------------:|-----|
| 1 | C1 (Sector-7)        | 145 | heaviest non-Earth |
| 2 | C6 (Sector-7-Outpost)| 15  | |
| 3 | C3 (Mars)            | 8   | |
| 4 | C2 (Sector-7)        | 6   | |
| 5 | C5 (Earth)           | 9999| **pinned bottom despite being the heaviest** |

The `Earth` row is also tinted blue (`tr.earth-row` in `src/styles.css`) so it's visually obvious.

### 5. Logout

Click **Log out** — the SPA clears the JWT from `localStorage` and routes back to `/login`. Refresh the page; you should land on `/login`, confirming session persistence is cleared.

## Production build sanity

```bash
cd frontend
npm run build      # tsc --noEmit && vite build → 42 modules transformed
npm run preview    # serves the built bundle on http://localhost:4173
```

## Submission email

- Subject: `Final Submission - Badhey - Portal Complete`
- Body: GitHub repo link + Loom/YouTube video link.
- Video name: `Final Submission - Badhey - Frontend Dashboard`. Recording must show **all four** of: Admin login (Upload visible + KG), logout, Standard login (no Upload in DOM + LBS), Earth row at the bottom. Include a webcam headshot per the PDF.
