from app.database.connection import get_connection
from psycopg2.extras import RealDictCursor


def execute_query(sql, params=None):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        conn.close()

def execute_write(sql, params=None):
    conn = get_connection()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            conn.commit()
    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

if __name__ == "__main__":
    print(execute_query("SELECT * FROM assets ORDER BY id"))