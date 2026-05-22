from app import init_db, DB_NAME


if __name__ == "__main__":
    init_db()
    print(f"PostgreSQL/Supabase database initialized: {DB_NAME}")
