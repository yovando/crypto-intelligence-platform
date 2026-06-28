CREATE TABLE IF NOT EXISTS assets (
    id SERIAL primary key,
    coingecko_id TEXT unique NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAUlT CURRENT_TiMESTAMP
);

CREATE TABLE IF NOt EXISTS price_history (
    id SERIAL primary key,
    asset_id INTEGER NOT NULL,
    price_usd NUMERIC NOT NULL,
    change_24h_pct NUMERIC,
    market_cap_usd BIGINT,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TiMESTAMP,

    FOREIGN KEY (asset_id) REFERENCES assets(id)
);

CREATE INDEX IF NOT EXISTS idx_price_history_asset_time
ON price_history (asset_id, recorded_at DESC);

CREATE TABLE IF NOT EXISTS news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    source TEXT,
    url TEXT UNIQUE,
    image_url TEXT,
    published_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TiMESTAMP

);

CREATE TABLE IF NOt EXISTS macro_data (
    id SERIAL PRIMARY KEY,
    indicator_name TEXT NOT NULL,
    value NUMERIC NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS portfolio (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL,
    quantity NUMERIC NOT NULL,
    buy_price_usd NUMERIC NOT NULL,
    bought_at TIMESTAMP NOt NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (asset_id) REFERENCES assets(id)
);
