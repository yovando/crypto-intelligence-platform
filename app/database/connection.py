import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def test_connection():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT 1")
    result = cur.fetchone()

    print(f"connected OK: {result[0]}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_connection()
