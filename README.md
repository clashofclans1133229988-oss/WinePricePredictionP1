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
 
