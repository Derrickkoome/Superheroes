# Superheroes Flask API

Simple Flask API for the Superheroes assignment.

Setup

1. Create a virtualenv and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Seed the database:

```bash
python seed.py
```

3. Run the app:

```bash
python app.py
```

Endpoints

- `GET /heroes`
- `GET /heroes/<id>`
- `GET /powers`
- `GET /powers/<id>`
- `PATCH /powers/<id>` (body: `{ "description": "..." }`)
- `POST /hero_powers` (body: `{ "strength": "Average", "power_id": 1, "hero_id": 3 }`)
