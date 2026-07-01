from app.database.connection import get_connection
from psycopg2.extras import RealDictCursor
from datetime import datetime

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
    execute_write(
        """
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
    rows = execute_query(
        """
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

def save_news_article(title, source, url, published_at, description, category, image_url):
    if published_at is not None:
        published_at = datetime.fromisoformat(
            published_at.replace("Z", "+00:00")
        )
    execute_write(
        """
        INSERT INTO news_articles (title, source, url, published_at, description, category, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (url)
        DO UPDATE
        SET
            image_url = EXCLUDED.image_url,
            description = EXCLUDED.description,
            category = EXCLUDED.category
        """, (title, source, url, published_at, description, category, image_url))

def save_news_articles(articles):
    for article in articles:
        try:
            save_news_article(
                article["title"],
                article["source"],
                article["url"],
                article["published_at"],
                article["description"],
                article["category"],
                article["image_url"])
        except Exception as e:
            print(f"Failed to save article '{article['title']}': {e}")

def get_recent_news(limit=10):
    return execute_query(
        """
        SELECT title, source, url, published_at, description, category, image_url
        FROM news_articles
        ORDER BY published_at DESC NULLS LAST
        LIMIT %s
        """, (limit,))

def get_balanced_news(crypto_limit=8, macro_limit=8):
    """Return a mix of crypto and macro headlines, newest first within each group."""
    crypto = execute_query(
        """
        SELECT title, source, url, published_at, description, category, image_url
        FROM news_articles
        WHERE category = 'crypto'
        ORDER BY published_at DESC NULLS LAST
        LIMIT %s
        """, (crypto_limit,))
    macro = execute_query(
        """
        SELECT title, source, url, published_at, description, category, image_url
        FROM news_articles
        WHERE category = 'macro'
        ORDER BY published_at DESC NULLS LAST
        LIMIT %s
        """, (macro_limit,))
    combined = list(crypto) + list(macro)
    combined.sort(key=lambda row: row["published_at"] or datetime.min, reverse=True)
    return combined

def save_briefing(content: str):
    execute_write(
        "INSERT INTO briefings (content) VALUES (%s)",
        (content,)
    )

def get_latest_briefing():
    rows = execute_query(
        """
        SELECT content, created_at FROM briefings
        ORDER BY created_at DESC
        LIMIT 1
        """
    )
    return rows[0] if rows else None

if __name__ == "__main__":
    print(execute_query("""SELECT category, COUNT(*) FROM news_articles GROUP BY category;"""))
    # print(get_recent_news())