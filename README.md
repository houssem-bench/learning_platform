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

## Default admin

- Username: `admin`
- Password: `admin123`

You can override these in `backend/.env`.
