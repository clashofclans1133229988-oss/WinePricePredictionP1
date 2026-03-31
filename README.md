# WinePricePredictionP1
This is a Flask-based wine price prediction app (machine learning model + web UI + REST API).

## Project structure
- `app.py`: main Flask app
- `models/`: pickled model and feature order
- `templates/`: Flask HTML frontend
- `data/`: original dataset and training scripts
- `docs/`: deployment + operation guides
- `.github/workflows/`: CI/CD pipeline

## Quick start
1. Create virtual env (locally):
   - `python -m venv .venv`
   - `source .venv/Scripts/activate` (Windows)
2. Install deps:
   - `pip install -r requirements.txt`
3. Run app:
   - `python app.py`
4. Open browser:
   - `http://localhost:5000`

## GitHub sync
- Keep this folder structure the same locally and on GitHub.
- `venvwp/` is ignored (not tracked) and should not be committed.

## Railway deployment (recommended, no credit card needed)
1. Sign up in Railway (https://railway.app) and connect GitHub.
2. In your repo, make sure `Dockerfile` is present and works locally:
   - `docker build -t wine-price-prediction .`
   - `docker run -p 5000:5000 wine-price-prediction`
   - `curl http://localhost:5000/`
3. Create a Railway project:
   - New project → Deploy from GitHub → select `WinePricePredictionP1` repository.
   - Choose deploy method: `Dockerfile` (or more direct if prompted).
4. Set Railway project name in GitHub secret:
   - Repository settings → Secrets and variables → Actions → `RAILWAY_PROJECT_NAME` = your-app-name (like `wine-price-prediction`).
5. (Optional) Add `RAILWAY_TOKEN` secret if you use Railway CLI in workflows.
6. Push to GitHub main and trigger workflows:
   - `git add . && git commit -m "Railway deploy config" && git push origin main`
7. In Railway dashboard, confirm deployment succeeded and note URL:
   - `https://<your-app-name>.railway.app`
8. Share this URL with your boss.

### Railway workflow in this repo
- `.github/workflows/docker.yml` builds and pushes Docker image to Docker Hub.
- `.github/workflows/deploy-railway.yml` triggers Railway deploy after Docker build.
- Ensure GitHub secrets are set: `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `RAILWAY_PROJECT_NAME`.

