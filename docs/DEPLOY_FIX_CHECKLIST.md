# Deploy Fix Checklist (Render)

Use this if Render fails before startup.

1. Open Render service dashboard.
2. Click **Manual Deploy** and select the **latest commit**.
3. Open **Settings → Build & Deploy**.
4. Confirm:
   - Root Directory: empty or `.`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Save and redeploy.

If the service is on free tier, first request after inactivity can be slow due to cold start.
