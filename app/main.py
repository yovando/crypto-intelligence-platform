from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from app.services.coingecko import (get_market_snapshot, get_top_movers, get_global_market)
from app.services.fear_greed import get_fear_greed
from app.database.queries import save_market_snapshot, get_price_history, save_news_articles, get_recent_news
from app.services.news import get_crypto_headlines


app = FastAPI()

templates = Jinja2Templates(directory=BASE_DIR/"templates")
app.mount("/static", StaticFiles(directory=BASE_DIR/"static"))

@app.get("/")
def home(request: Request):
    snapshot_data = fetch_market_data()
    news_data = fetch_news_data()
    return templates.TemplateResponse(
        request = request,
        name = "dashboard.html",
        context = {
            "snapshot": snapshot_data["snapshot"],
            "gainers": snapshot_data["gainers"] if snapshot_data["gainers"] else None,
            "losers": snapshot_data["losers"] if snapshot_data["losers"] else None,
            "fg": snapshot_data["fg"],
            "global_market": snapshot_data["global_market"],
            "news_data": news_data
        }
    )

@app.get("/api/market")
def api_market():
    return fetch_market_data()

@app.get("/health")
def health():
    return "OK"

@app.get("/api/prices/{symbol}")
def api_prices(symbol: str, limit: int = 100):
    return get_price_history(symbol.upper(), limit)

@app.get("/api/news")
def api_news():
    return fetch_news_data()

def fetch_market_data():
    snapshot = get_market_snapshot()
    if snapshot:
        try:
            save_market_snapshot(snapshot)
        except Exception as e:
            print(f"failed to save market snapshot: {e}")

    movers = get_top_movers()
    fg = get_fear_greed()
    global_market = get_global_market()

    return {
        "snapshot": snapshot,
        "gainers": movers["gainers"] if movers else None,
        "losers": movers['losers'] if movers else None,
        "fg": fg,
        "global_market": global_market,
    }

def fetch_news_data():
    articles = get_crypto_headlines()
    if articles:
        try:
            save_news_articles(articles)
        except Exception as e:
            print(f"failed to save news: {e}")
    try:
        return get_recent_news(limit=15)
    except Exception as e:
        print(f"failed to load news: {e}")
        return None
