# PPII 2023 – Recycling Map Web App

This project is a web app that helps users recycle more by showing nearby recycling locations on a map based on their current position. The goal is to reduce non-recycled waste by making it simple to find where to bring different types of waste. Users can explore centers, leave comments, and manage a basic profile.

## Features
- Interactive map of nearby recycling centers
- Center-specific comments and waste types
- Simple registration, login, and profile (visits, comments, favorites)
- Flask + SQLite backend, HTML/CSS/JS frontend

## Tech Stack
- Backend: Python (Flask), SQLite
- Frontend: HTML, CSS, JavaScript
- Templates and static assets in `templates/` (static under `templates/static/`)

## Prerequisites
- Windows 10/11
- Python 3.9+ installed and on PATH (`py -3 --version`)
- (Optional) Git

## Getting Started (Windows)

1) Clone and move into the folder:
```
git clone <your-repo-url>
cd PPII_2023
```

2) Create and activate a virtual environment (PowerShell):
```
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Install dependencies:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4) Prepare the SQLite database:
- The app expects: `data/info.db`. Create the folder and an empty DB:
```
python -c "import os, sqlite3; os.makedirs('data', exist_ok=True); sqlite3.connect('data/info.db').close()"
```
- Initialize tables according to your schema. If you don’t have one yet, you can start with a minimal schema like:
```
-- init_db.sql (example)
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  login TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  visits INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS centers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  latitude REAL,
  longitude REAL
);

CREATE TABLE IF NOT EXISTS comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_client INTEGER NOT NULL,       -- should reference users.id
  waste_type TEXT NOT NULL,
  comment TEXT NOT NULL,
  date TEXT NOT NULL,
  center_id INTEGER NOT NULL,       -- should reference centers.id
  FOREIGN KEY (id_client) REFERENCES users(id),
  FOREIGN KEY (center_id) REFERENCES centers(id)
);

CREATE TABLE IF NOT EXISTS fav (
  id_client INTEGER NOT NULL,       -- users.id
  id_center INTEGER NOT NULL,       -- centers.id
  PRIMARY KEY (id_client, id_center),
  FOREIGN KEY (id_client) REFERENCES users(id),
  FOREIGN KEY (id_center) REFERENCES centers(id)
);
```
Then apply it to your DB (PowerShell):
```
sqlite3 data/info.db ".read init_db.sql"
```

5) Run the app:
- Easiest:
```
python app.py
```
- Or with Flask CLI (auto-reload in development):
```
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"
flask run
```

6) Open in your browser:
- http://localhost:5000
- Allow location access in your browser so the map can center on your position.

## Project Structure
```
app.py                    # Flask app (routes, DB access)
templates/                # Jinja templates and static assets
  *.html
  static/
    images/
    scripts/
    styles/
data/
  info.db                 # SQLite database (created by you)
```

## Key Routes
- GET /                → Homepage
- GET /map             → Map of recycling centers
- GET /dons            → Donations info page
- GET /register        → Registration form
- POST /register       → Create account
- GET /login           → Login form
- POST /login          → Authenticate and increment visits
- GET /profile         → User profile (requires login)
- GET /<center_id>/comments
- POST /<center_id>/add_comment

## Notes
- Geolocation works on localhost but needs user permission.
- Database path is configured in `app.py` as `data/info.db`.
- Ensure your table/column names match the queries used in `app.py`.

## Development Tips
- Keep your virtual environment out of Git by adding `.venv` to `.gitignore`.
- If you change templates or static files, Flask debug mode will auto-reload the server.
