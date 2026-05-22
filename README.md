# Paraiso Ala Eh Python Flask - Supabase/PostgreSQL Version

This project uses **Python Flask** for the backend and **Supabase PostgreSQL** for the database.

## Main files

```text
app.py                Main Flask app and routes
database/schema.sql   PostgreSQL table schema for Supabase
requirements.txt      Python dependencies
render.yaml           Render deployment config
wsgi.py               Gunicorn entry point
```

## Default test accounts

Admin login:

```text
Username: admin
Password: admin123
```

Guest login for booking:

```text
Email: user@gmail.com
Password: 12345
```

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set your `DATABASE_URL`.
4. Initialize the database tables:

```bash
python init_db.py
```

5. Run the app:

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

## Render + Supabase setup

1. Create a Supabase project.
2. Go to **Supabase Dashboard > Project Settings > Database**.
3. Copy the PostgreSQL connection string/URI.
4. In Render, open your web service, then go to **Environment**.
5. Add or update these environment variables:

```text
DATABASE_URL=postgresql://postgres:your-password@db.your-project-ref.supabase.co:5432/postgres
DB_SSLMODE=require
AUTO_INIT_DB=true
DB_CREATE_IF_MISSING=false
FLASK_DEBUG=0
APP_DEBUG=false
```

6. Redeploy the Render service.

The app will automatically create the required tables and seed the default admin/rooms when it starts.

## Important notes

- This version is for **Supabase/PostgreSQL**, not MySQL.
- If your Supabase password has special characters, copy the exact URL from Supabase or URL-encode the password.
- If Render logs show connection errors, double-check `DATABASE_URL`, database password, and `DB_SSLMODE=require`.
