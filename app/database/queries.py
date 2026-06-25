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

def get_asset_id_by_coingecko_id(coingecko_id: str):
    coin_id = execute_query("SELECT id FROM assets WHERE coingecko_id = %s", (coingecko_id,))
    if not coin_id:
        return None
    return coin_id[0]["id"]

def save_price_snapshot(asset_id, price_usd, change_24h_pct, market_cap_usd):
    execute_write("""
                  INSERT INTO price_history (asset_id, price_usd, change_24h_pct, market_cap_usd)
                  VALUES (%s, %s, %s, %s)
                  """, (asset_id, price_usd, change_24h_pct, market_cap_usd))

def save_market_snapshot(snapshot):
    rows = execute_query("SELECT id, coingecko_id FROM assets")

    asset_map = {
        row["coingecko_id"]: row["id"]
        for row in rows}

    for coin in snapshot:
        asset_id = asset_map.get(coin["id"])
        if asset_id is not None:
            save_price_snapshot(
                asset_id, 
                coin["price_usd"], 
                coin["change_24h"], 
                coin["market_cap_usd"])

    # for coin in snapshot:
    #     asset_id = get_asset_id_by_coingecko_id(coin["id"])
    #     if asset_id is not None:
    #         save_price_snapshot(asset_id, coin["price_usd"], coin["change_24h"], coin["market_cap_usd"])

def get_price_history(symbol, limit=100):
    rows = execute_query("""
                        SELECT p.price_usd, p.change_24h_pct, p.market_cap_usd, p.recorded_at
                        FROM price_history p
                        JOIN assets a ON a.id = p.asset_id
                        WHERE a.symbol = %s
                        ORDER BY p.recorded_at DESC
                        LIMIT %s
                        """, (symbol, limit))
    return {
        "symbol": symbol,
        "history":[
            {
                "price_usd": row["price_usd"],
                "change_24h_pct": row["change_24h_pct"],
                "market_cap_usd": row["market_cap_usd"],
                "recorded_at": row["recorded_at"]}
                for row in rows
        ]
    }
    

if __name__ == "__main__":
    print(execute_query("""
                        SELECT a.symbol, p.price_usd, p.recorded_at
                        FROM price_history p
                        JOIN assets a ON a.id = p.asset_id
                        ORDER BY p.recorded_at DESC
                        LIMIT 10;
                        """))