from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from app.services.coingecko import (get_coin_data, get_market_snapshot, get_top_movers)

app = FastAPI()

templates = Jinja2Templates(directory=BASE_DIR/"templates")
app.mount("/static", StaticFiles(directory=BASE_DIR/"static"))

@app.get("/")
def home(request: Request):
    
    snapshot = get_market_snapshot()
    movers = get_top_movers()
    
    if snapshot is None or movers is None:
       return templates.TemplateResponse(
            request = request,
            name = "dashboard.html",
            context = {
                "error": "Market data unavailable"
            }
        )
    else:
        return templates.TemplateResponse(
            request = request,
            name = "dashboard.html",
            context = {
                "snapshot": snapshot,
                "gainers": movers["gainers"],
                "losers": movers["losers"],
                "error": None
            }
        )

@app.get("/health")
def health():
    return "OK"