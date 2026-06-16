from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from app.services.coingecko import (get_market_snapshot, get_top_movers, get_global_market)
from app.services.fear_greed import get_fear_greed


app = FastAPI()

templates = Jinja2Templates(directory=BASE_DIR/"templates")
app.mount("/static", StaticFiles(directory=BASE_DIR/"static"))

@app.get("/")
def home(request: Request):
    data = fetch_market_data()
    return templates.TemplateResponse(
        request = request,
        name = "dashboard.html",
        context = {
            "snapshot": data["snapshot"],
            "gainers": data["gainers"] if data["gainers"] else None,
            "losers": data["losers"] if data["losers"] else None,
            "fg": data["fg"],
            "global_market": data["global_market"]
        }
    )

@app.get("/api/market")
def api_market():
    return fetch_market_data()

@app.get("/health")
def health():
    return "OK"

def fetch_market_data():
    snapshot = get_market_snapshot()
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