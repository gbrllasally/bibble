# PR Conflict Fix Guide

If GitHub says your PR has conflicts, it means your branch and target branch changed the same lines.

## Easiest way (no terminal): GitHub UI
1. Open your PR page.
2. Click **Resolve conflicts**.
3. For each conflict block:
   - keep your version,
   - keep incoming version,
   - or combine both manually.
4. Click **Mark as resolved** for each file.
5. Click **Commit merge**.
6. PR should become mergeable.

## Safer way (recommended): update branch from latest main
Run these commands in your local repo:

```bash
git checkout <your-branch>
git fetch origin
git merge origin/main
```

If conflicts appear:
1. Open conflicted files.
2. Find markers like:
   - `<<<<<<< HEAD`
   - `=======`
   - `>>>>>>> origin/main`
3. Edit file to final desired content.
4. Remove conflict markers.

Then finish:

```bash
git add .
git commit -m "Resolve merge conflicts with main"
git push
```

GitHub PR will auto-refresh after push.

## If you just want the quickest clean path
Create a fresh branch from latest main and re-apply your changes:

```bash
git checkout main
git pull
git checkout -b fix/new-pr-clean
# copy/re-apply your changes
git add .
git commit -m "Reapply changes on fresh branch"
git push -u origin fix/new-pr-clean
```

Then open a new PR from that branch.
