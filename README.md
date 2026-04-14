# Alkitab Teman Hati (Beginner-Friendly Setup Guide)

This project is a **Python/FastAPI web app** for Indonesian end users.
Users type their feelings in Indonesian, and the app returns:
- a short empathetic reflection,
- suggested Bible verses,
- a simple reading plan.

You can add Telegram later, but start with the web app first.

---

## Is this a web app or a Telegram bot?
It can be both, but right now:
- ✅ **Web app is ready**
- 🟨 Telegram webhook endpoint exists, but full bot flow is next

So: deploy web app first, then connect Telegram.

---

## Easiest free deployment: Render

## 1) Put this code on GitHub
1. Create a GitHub account.
2. Create a new repository.
3. Upload this project to that repository.

## 2) Create a Render Web Service
1. Go to [https://render.com](https://render.com) and sign in.
2. Click **New +** (top-right).
3. Click **Web Service**.
4. Connect/select your GitHub repo.
5. Render opens a **"Create Web Service"** form.

In that form, set:
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Then click **Create Web Service**.

> If you said you cannot find Build/Start settings: they are inside the **Create Web Service** page, usually in the **Build & Deploy** section.

---

## Where to find Build Command / Start Command after service is created
If your service already exists:
1. Open your service in Render dashboard.
2. Click **Settings**.
3. Find **Build & Deploy**.
4. Edit these fields:
   - **Build Command**
   - **Start Command**
5. Click **Save Changes** and redeploy.

---

## How to test (non-technical)
After deploy is Live:
1. Open your Render URL.
2. Type: `Saya cemas soal masa depan.`
3. Click **Kirim Curhat**.
4. You should see reflection + verse suggestions + reading plan.

If you see those, your app is working.

---

## Optional local run (for technical helper)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Open: `http://localhost:8000`

---

## Vercel (free) vs Render (free)
- **Vercel Hobby** is free, but it is more optimized for frontend/serverless workflows.
- For this current **Python FastAPI backend**, **Render is usually simpler**.

Recommended path:
1. Deploy full app on Render first.
2. Later, if needed, host frontend elsewhere and keep backend on Render.

---

## Project files
- `app/main.py` → backend logic + API endpoints
- `templates/index.html` → browser UI
- `data/alkitab_tb_sample.json` → sample verse data
- `tests/test_app.py` → basic tests

---

## Licensing note
If you plan to use full "Alkitab Terjemahan Baru" text in production,
make sure you have the proper license/permission from the rights holder.

## Render build failed with: "Could not open requirements.txt"
This specific error usually means Render built the **wrong commit** or wrong root settings.

Use this checklist:
1. In Render, open your service → **Manual Deploy** → choose the latest commit (not the old `Initialize repository` commit).
2. Confirm repo root has `requirements.txt` (this repo now has it at root).
3. In Render service **Settings**:
   - **Root Directory** should be empty (or `.`)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Click **Save Changes** and redeploy.

Also: free Render instances can sleep when inactive. The first request after idle can be slow (cold start). That is expected on free tier.

This repo now includes `render.yaml` and `.python-version` to make deployment settings more explicit.


## Product updates
- Added reset button in UI.
- Chat now returns multiple verses with randomized selection so repeated prompts can return different verses.
- Added optional long-passage mode (`include_long_passages`).
- Replaced reading plan with generated closing prayer.

## How to provide full Bible knowledge base
You can now import your full Bible file into a local SQLite knowledge base.

1. Prepare JSON or CSV with columns/fields: `book`, `chapter`, `verse`, `text`, optional `reference`.
2. Run importer:
   ```bash
   python scripts/build_bible_kb.py --input /path/to/alkitab_tb.json --format json --translation TB
   ```
3. This builds `kb/bible.db`.
4. App will automatically use `kb/bible.db` for retrieval; if DB is missing, it falls back to sample JSON.

See full guide: `docs/BIBLE_KB_SETUP.md`.
