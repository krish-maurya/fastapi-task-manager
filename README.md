# Full-Stack Backend Internship Assignment

This project is a complete full-stack implementation for a Backend Developer Internship assignment.

## Tech Stack

- Backend: FastAPI + SQLAlchemy ORM
- Database: PostgreSQL
- Authentication: JWT (access + refresh)
- Frontend: React (Vite)
- Testing: pytest
- API Docs: Swagger via FastAPI
- Bonus: Docker Compose + Redis container

## Project Structure

```text
backend/
  app/
    main.py
    core/
      config.py
      deps.py
      exceptions.py
      logging_config.py
      security.py
    db/
      base.py
      session.py
    models/
      task.py
      user.py
    routes/
      auth.py
      tasks.py
      utils.py
    schemas/
      common.py
      task.py
      token.py
      user.py
    services/
      auth_service.py
      external_service.py
      task_service.py
  tests/
    conftest.py
    test_auth.py
    test_tasks.py
  requirements.txt
  postman_collection.json

frontend/
  src/
    components/
      AuthForm.jsx
      TaskForm.jsx
      TaskList.jsx
    pages/
      DashboardPage.jsx
      LoginPage.jsx
      RegisterPage.jsx
    services/
      api.js
    App.jsx
    main.jsx
    styles.css
```

## Backend Setup

1. Go to backend directory:

```bash
cd backend
```

2. Create virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Create `.env` file from template:

```bash
copy .env.example .env
```

4. Ensure PostgreSQL is running and matches `DATABASE_URL`.

5. Run backend server:

```bash
uvicorn app.main:app --reload
```

Server URL: `http://localhost:8000`

Swagger docs: `http://localhost:8000/docs`

## Frontend Setup

1. Go to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Run frontend:

```bash
npm run dev
```

Frontend URL: `http://localhost:5173`

To point to a custom backend API, set:

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Environment Variables (Backend)

- `APP_NAME`
- `APP_ENV`
- `API_V1_PREFIX`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
- `DATABASE_URL`
- `FRONTEND_ORIGIN`
- `EXTERNAL_API_URL`
- `REDIS_URL`

## API Endpoints

Base path: `/api/v1`

Authentication:
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`

Tasks:
- `POST /tasks` (authenticated)
- `GET /tasks` (authenticated)
- `GET /tasks/{task_id}` (authenticated + owner/admin)
- `PUT /tasks/{task_id}` (authenticated + owner/admin)
- `DELETE /tasks/{task_id}` (admin only)

Utilities:
- `GET /utils/external-check` (retry + timeout demo)

## Security Features

- Password hashing with bcrypt via Passlib
- JWT access and refresh token validation
- RBAC with `user` and `admin`
- Input validation with Pydantic
- Basic input sanitization for task text fields

## Testing

From `backend/`:

```bash
pytest
```

Test coverage includes:
- Auth registration/login/refresh
- Task CRUD rules (user vs admin delete permissions)

## Postman Collection

Import this file in Postman:

`backend/postman_collection.json`

## Docker Setup

From project root:

```bash
docker compose up --build
```

This starts:
- PostgreSQL on `5432`
- Redis on `6379`
- Backend on `8000`
- Frontend on `5173`

## Notes

- SQLAlchemy creates tables on startup for quick onboarding.
- For production, use Alembic migrations and stronger secret management.
