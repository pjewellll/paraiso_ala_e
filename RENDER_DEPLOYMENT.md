# Render Deployment with Supabase PostgreSQL

## 1. Create a Supabase database

1. Open Supabase and create a project.
2. Go to **Project Settings > Database**.
3. Copy the PostgreSQL connection string.

Use the direct connection string if available. It usually looks like:

```text
postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
```

## 2. Configure Render environment variables

In Render, open your web service and go to **Environment**. Set:

```text
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
DB_SSLMODE=require
AUTO_INIT_DB=true
DB_CREATE_IF_MISSING=false
APP_HOST=0.0.0.0
APP_DEBUG=false
FLASK_DEBUG=0
SECRET_KEY=your-random-secret-key
```

Do not use the old MySQL variables (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`) unless you are running local PostgreSQL without `DATABASE_URL`.

## 3. Build and start commands

Render should use:

```text
Build Command: pip install --upgrade pip && pip install -r requirements.txt
Start Command: gunicorn wsgi:app
```

## 4. Redeploy

After saving the environment variables, click:

```text
Manual Deploy > Deploy latest commit
```

## 5. Verify

Open your site and check:

```text
/healthz
```

It should return:

```json
{"status":"ok"}
```

## Troubleshooting

### `PostgreSQL/Supabase connection failed`

Check `DATABASE_URL`, password, and `DB_SSLMODE=require`.

### `password authentication failed`

The Supabase database password is wrong. Reset/copy the database password from Supabase.

### `connection timeout`

Use the correct Supabase connection string and make sure the database project is active.

### Tables are missing

Make sure `AUTO_INIT_DB=true`, then redeploy. You can also run locally:

```bash
python init_db.py
```
