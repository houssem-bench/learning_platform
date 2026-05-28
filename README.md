# Learning Platform

Full-stack learning platform with FastAPI + React and seeded Unity QCU quizzes.

## Backend

```bash
cd learning_platform/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend

```bash
cd learning_platform/frontend
npm install
npm run dev
```

## Render deployment

This repo includes a Render Blueprint at [render.yaml](render.yaml) that creates:

- A FastAPI web service with a persistent disk for SQLite.
- A static site for the Vite frontend with SPA rewrites.

Steps:

1. In Render, create a new Blueprint and point it at this repo.
2. After services are created, verify the env vars:
	- `VITE_API_BASE` points at your API service URL.
	- `CORS_ORIGINS` includes your frontend URL (comma-separated).

If you rename the services, update the URLs in Render to match.

## Default admin

- Username: `admin`
- Password: `admin123`

You can override these in `backend/.env`.
