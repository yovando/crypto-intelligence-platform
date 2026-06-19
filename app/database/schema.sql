CREATE TABLE IF NOT EXISTS assets (
    id SERIAL primary key,
    coingecko_id TEXT unique NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAUlt CURRENT_TiMESTAMP
);

CREATE TABLE IF NOt EXISTS price_history (
    id SERIAL primary key,
    asset_id INTEGER NOT NULL,
    price_usd NUMERIC NOT NULL,
    change_24h_pct NUMERIC,
    market_cap_usd INTEGER,
    recorded_at tiMESTAMP NOt NULL DEFAULT CURRENT_TiMESTAMP,

    FOREIGN KEY (asset_id) REFERENCES assets(id)
);

CREATE TABLE IF NOT EXISTS news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    source TEXT,
    url TEXT UNIQUE,
    published_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TiMESTAMP

)