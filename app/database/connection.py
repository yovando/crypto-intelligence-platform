import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def test_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")
    
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur = conn.cursor()
                cur.execute("SELECT 1")
                result = cur.fetchone()

                print(f"connected OK: {result[0]}")

    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_connection()
