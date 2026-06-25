from app.services.coingecko import TRACKED_COINS
from app.database.connection import get_connection

def seed_assets():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for coin in TRACKED_COINS:
                cursor.execute("""
                            INSERT INTO assets (coingecko_id, symbol, name)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (coingecko_id) DO NOTHING
                            """, (coin["id"], coin["symbol"], coin["name"]))
        conn.commit()
    
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
if __name__ == "__main__":
    seed_assets()