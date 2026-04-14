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

## If deploy says "exited with status 1"
1. Open Render logs and find the **first** error line (not the last line).
2. If it fails in build step, check the printed line from `scripts/render_build.sh`:
   - current working directory,
   - whether `requirements.txt` exists.
3. If `requirements.txt` missing, fix **Root Directory** to empty or `.` and redeploy.
4. If package install fails, paste the exact package error line and version number.
