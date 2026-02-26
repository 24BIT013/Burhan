# School Management System

This project is now split into:

- `backend/`: Django project, apps, migrations, dependencies, and runtime entry points (Render).
- `frontend/`: Next.js frontend app for Vercel, plus the existing Django templates/static used by backend rendering.

## Backend local run

1. Create and activate a virtual environment (optional).
2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

## Frontend local run

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Configure backend URL:
   - Create `frontend/.env.local` with:
   ```bash
   NEXT_PUBLIC_BACKEND_URL=https://burhan-2.onrender.com
   ```
3. Run frontend:
   ```bash
   npm run dev
   ```

## Deploy

- Render (backend):
  - Root Directory: `backend`
  - Build Command: `bash build.sh`
  - Start Command: `gunicorn burhan.wsgi:application --bind 0.0.0.0:$PORT`
- Vercel (frontend):
  - Root Directory: `frontend`
  - Framework: Next.js
  - Build Command: `npm run build`
  - Env var: `NEXT_PUBLIC_BACKEND_URL`

