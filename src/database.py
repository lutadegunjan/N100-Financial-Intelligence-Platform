from sqlalchemy import create_engine, text
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATABASE_NAME = os.path.join(BASE_DIR, "db", "nifty100.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "db", "schema.sql")

engine = create_engine(f"sqlite:///{DATABASE_NAME}")

def create_tables():
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema = f.read()

    with engine.begin() as conn:
        for statement in schema.split(";"):
            if statement.strip():
                conn.execute(text(statement))

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")