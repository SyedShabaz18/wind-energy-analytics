# WindCast Analytics — Gridbricks Full Stack SWE Challenge 

A React + Python FastAPI pilot web app to evaluate UK national wind generation forecasts against Elexon actual generation. January **2026 purchasing decisions**, including January 31 → February 1 delivery.

> **Important:** The app does **not** predict wind output, trade power, or estimate a utility's electricity purchase volume. It compares published wind forecasts with observed output. The decision cutoff is an explicit illustrative assumption; the assignment does not provide an actual procurement deadline.

## Quick start (Windows / VS Code, no Docker needed)

Prerequisites: Python 3.11+, Node.js 20+, npm.

**Terminal 1 — backend** (from repository root):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Check http://localhost:8000/docs and http://localhost:8000/api/health.

**Terminal 2 — frontend** (new VS Code terminal, from repository root):

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Start in **Live Elexon API** mode; switch to **Synthetic UI preview** to inspect the layout without the API. **Synthetic mode is fictional and must not be presented as Elexon results.**

If the backend runs on a different host, copy `frontend/.env.example` to `frontend/.env` and change `VITE_API_URL`, then restart Vite.

## Docker (once Docker Desktop Engine is running)

```powershell
docker compose up --build
```

Frontend http://localhost:5173; backend http://localhost:8000/docs.

## Directory map

- `frontend/src/App.jsx`: dashboard, charts, filters, error and loading states, CSV export.
- `frontend/src/styles.css`: responsive design.
- `frontend/src/demo.js`: **explicitly synthetic** UI-preview records.
- `frontend/.env.example`: public API URL configuration.
- `backend/app/main.py`: API routes and January 2026 validation.
- `backend/app/elexon.py`: HTTP retrieval of Elexon BMRS datasets.
- `backend/app/analytics.py`: cutoff selection, time alignment, metrics.
- `backend/tests/test_analytics.py`: pure-function unit tests.
- `docker-compose.yml`, `*/Dockerfile`: container setup.
- `backend/Procfile`: Heroku process definition.

## API

- `GET /api/health` — status.
- `GET /api/analysis?decision_date=2026-01-15&cutoff_hour=11` — fetch and analyze a decision date.
- `GET /docs` — FastAPI interactive documentation.

## Business interpretation and assumptions

1. Select a **decision date** in January 2026, and an illustrative decision cutoff, default **11:00 Europe/London** on that date. This is **not claimed** to be the official UK day-ahead auction deadline. The user can choose a different cutoff.
2. The delivery date is the **next UK calendar day**. A January 31 decision targets February 1 delivery. All interval alignment is done in UTC; UK calendar boundaries use `Europe/London` to account for DST.
3. Retrieve actual records from **FUELHH**, keeping only `fuelType = WIND`, and forecasts from **WINDFOR**.
4. For each half-hour `startTime` in the delivery day, choose the forecast with the **latest `publishTime` no later than the cutoff**. Do not use later forecasts (prevents look-ahead bias).
5. Pair with actual generation on `startTime`. Missing actual or eligible forecast is **not** treated as zero and is excluded from error metrics. Report coverage.
6. Forecast retrieval uses a **7-day lookback** relative to the decision cutoff as a pragmatic pilot limit; this is a modeling choice, not a guarantee about Elexon's full forecast history.
7. Signed error is `forecast − actual`. Positive = overforecast. **MAE** is mean absolute error in MW; **RMSE** is root mean square error in MW; **bias** is mean signed error in MW; **WAPE** = sum absolute errors / sum absolute actual generation × 100 (undefined if denominator is zero).
8. MW is **power**, not energy. Half-hour MW readings are not summed and presented as MWh.
9. The assignment permits only Elexon national wind data; consumer demand and other generation are out of scope, so the app **cannot calculate net power to buy**.

## Upstream API and reliability

Elexon BMRS base: `https://data.elexon.co.uk/bmrs/api/v1`.

- `GET /datasets/FUELHH/stream` with `from`, `to`, `format=json`.
- `GET /datasets/WINDFOR/stream` with `from`, `to`, `format=json`.

The app requests in daily UTC chunks and retries transient errors. Elexon API shape/availability and historical WINDFOR coverage **must be verified against the live API before submitting**; the included code has been prepared without asserting a successful live API test. If the provider changes endpoint parameters or data availability, adapt `backend/app/elexon.py`. Large historical windows can be slow; production would benefit from caching and scheduled ingestion.

## Tests

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

Unit tests cover no future-forecast leakage, missing-data handling, and Jan 31 delivery rollover. Also manually check several dates against Elexon, including empty-data states, before submission.

## Deploy (Vercel frontend + Heroku backend)

**Backend:** Create a Heroku app using the `backend/` directory as app root (e.g. deploy it separately with `git subtree` or a dedicated backend repository), select Python buildpack or container deployment, and set `CORS_ORIGINS=https://YOUR-FRONTEND.vercel.app`. Heroku may require a paid plan. Ensure the API health URL works publicly.

**Frontend:** In Vercel, import the repository, set **Root Directory** to `frontend`, framework **Vite**, build command `npm run build`, output directory `dist`. Add environment variable `VITE_API_URL=https://YOUR-BACKEND.herokuapp.com` (no trailing slash), deploy and test. The `frontend/vercel.json` provides SPA fallback.

**Deployment URL:** _Replace this with the real Vercel URL before submission._

**Backend URL:** _Replace this with the real backend URL before submission._

**Video URL:** _Replace with your unlisted YouTube demo link before submission._

## Submission checklist

- [ ] Verify live Elexon results, cutoff semantics, and actual/forecast match rates.
- [ ] Run unit tests and inspect real API responses.
- [ ] Confirm Docker Engine starts and `docker compose up --build` works.
- [ ] Deploy both services and set production CORS + VITE_API_URL.
- [ ] Create public GitHub repository with **anonymous/random name** (per assignment).
- [ ] Record max **10-minute** unlisted YouTube video: client pitch (≤5 min) + technical review (≤5 min).
- [ ] Test repo, deployed app, and YouTube links in incognito before submitting form.

## AI assistance disclosure

**AI tools were used** to assist with application scaffolding, UI styling, implementation, unit-test examples, and README drafting. The developer is responsible for reviewing the code, verifying live Elexon integration, testing, deployment, and explaining the implementation in the technical video.

## Limitations / next steps

No caching or persistent DB; repeated requests can be slow. No real-time streaming, demand data, or price data. The decision cutoff is illustrative. Live upstream API behavior is subject to verification. Potential improvements: scheduled historical ingestion, server caching, monthly summary, and richer coverage diagnostics.

## Version 2 — corrections and verification status

- Corrected raw dataset query parameters: WINDFOR stream is queried by `publishDateTimeFrom`/`publishDateTimeTo`; FUELHH dataset by `settlementDateFrom`/`settlementDateTo`.
- WINDFOR is fetched up to the selected cutoff, with a documented seven-day publication lookback. Delivery timestamps are matched after ingestion.
- Added Windows `tzdata` dependency, extra tests and a visible no-matched-data warning with upstream record counts.
- **Verification limitation:** This packaged version has not been tested against live Elexon from the packaging environment. Verify live data and deployment before submitting. Do not present synthetic preview as observed data.
- Elexon WINDFOR provides a set of forecast target timestamps, which may be sparser than every half-hour. Unmatched periods remain missing; the UI reports coverage rather than interpolating or inventing values.

## Version 3 navigation and date selection
- Sidebar sections: Overview, Generation charts, Forecast accuracy, Half-hourly records, Elexon data sources.
- Chart page has line/area chart style controls and forecast-error bars; values are plotted continuously, while hover tooltips provide precise readings.
- The decision date selector permits 2022–2026 for optional exploration. **The assignment's evaluated purchasing-decision scope is January 2026**, so other dates are clearly labeled exploratory; historical availability is not guaranteed.
- Elexon data sources is an informational page; it does not assert any missing data has been resolved.
- If `npm install` was already run for the earlier version, run `npm install` in the new frontend and `npm run dev` as usual. Keep the backend running separately.


## Final reviewed build notes (2026-10-26)

**Assignment scope:** January 2026 UK-local purchase decision dates, with delivery on the following UK-local day. Other dates in the picker are optional exploration only. The cutoff is an illustrative assumption, **not** an official day-ahead gate-closure time. Wind generation alone does not determine the utility's full procurement quantity.

**Data source:** Only Elexon BMRS FUELHH actual generation (filtered to `fuelType=WIND`) and WINDFOR published forecasts. The backend uses the FUELHH non-stream dataset with settlement-date filters, which returns the same dataset, and WINDFOR stream with publication-window filters. The latter searches a seven-day historical publication window; if forecasts are unavailable within that lookback, coverage is reported as missing. Only forecasts with `publishTime <= cutoff` are eligible. Averages and errors use only matched intervals; missing data is never substituted with zero. Daylight-saving days can have 46 or 50 intervals.

**Docker:** `docker compose up --build` from the project root. Open http://localhost:8080. The Docker frontend uses a production Vite build served by Nginx and reverse-proxies API calls to the Python backend. Docker Compose does not require local Python or Node. Docker build/run is **not verified** in the packaging environment.

**Local development:** Start backend on port 8000 and `npm run dev` from frontend on port 5173. Use `npm run build` to check the production frontend bundle. Run backend tests with `python -m pytest -q` inside the backend environment.

**Deploy:** A hosted frontend needs `VITE_API_URL` set to the public HTTPS backend origin **at build time**, and backend `CORS_ORIGINS` set to the deployed frontend HTTPS origin. Never deploy the Nginx Docker proxy configuration to Vercel as-is; the frontend directory's Vite build is the Vercel target. Choose a backend host that supports FastAPI (e.g. Heroku), then test both live URLs. Add your actual deployed link here before submitting: **DEPLOYED_URL: NOT YET AVAILABLE**.

**Security:** No authentication is needed for this read-only pilot. Public production APIs still require external rate limiting, HTTPS, logging, and dependency vulnerability scans. Backend errors intentionally avoid returning upstream exception text. In-memory cache is bounded to 64 queries and expires after 1 hour. Do not commit `.env`, `.venv`, or `node_modules`.

**Testing limitations:** Unit tests use mocked Elexon records and verify time alignment, DST, missing values, and look-ahead prevention. A live Elexon API integration test, Docker runtime check, dependency audit, and public deployment verification could not be completed from the offline packaging environment; these must be completed before submission. The synthetic UI preview is not evidence of real Elexon accuracy.

**AI assistance disclosure:** This project was built and revised with assistance from OpenAI ChatGPT, including frontend/backend code generation, code review, testing, documentation, and troubleshooting. The applicant must review the final deliverables and explain the implementation in the submission video.
