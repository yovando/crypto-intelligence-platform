from app.database.connection import get_connection


def execute_query(sql, params=None):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
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

    finally:
        conn.close()

if __name__ == "__main__":
    print(execute_query("SELECT COUNT(*) FROM assets;"))