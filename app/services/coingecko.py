import requests
import os
from dotenv import load_dotenv

load_dotenv()
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

TRACKED_COINS = [
    {
    "id": "bitcoin",
    "name": "Bitcoin",
    "symbol": "BTC"},
    {
    "id": "ethereum",
    "name": "Ethereum",
    "symbol": "ETH"},
    {
    "id": "solana",
    "name": "Solana",
    "symbol": "SOL"},
    {
    "id": "ripple",
    "name": "Ripple",
    "symbol": "XRP"},
    {
    "id": "binancecoin",
    "name": "Binancecoin",
    "symbol": "BNB"},
]
    

def fetch_price_json(id_list):
    headers = {
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }

    if isinstance(id_list, list):
        id_list = ",".join(id_list)

    params = {
    "vs_currencies": "usd",
    "ids": id_list,
    "include_24hr_change": "true",
    "include_market_cap": "true"
    }

    try:
        http_response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params=params,
            headers=headers,
            timeout=10)
        
        if not http_response.ok:
            return None
        
        return http_response.json()
    
    except (requests.RequestException, ValueError):
        return None
    
def get_coin_data(coin_id: str):
    coin_id = coin_id.strip().lower()
    if coin_id == "":
        return None
    
    data = fetch_price_json(coin_id)

    if not data:
        return None
    
    coin_data = data.get(coin_id)
    if not coin_data:
        return None
    
    price_usd = coin_data.get("usd")
    market_cap_usd = coin_data.get("usd_market_cap")
    change_24h_usd = coin_data.get("usd_24h_change")

    if not price_usd or not market_cap_usd or change_24h_usd is None:
        return None

    return {
        "id": coin_id,
        "price_usd": price_usd,
        "market_cap_usd": market_cap_usd,
        "change_24h": change_24h_usd
    }

def get_market_snapshot():
    list_id = [coin["id"] for coin in TRACKED_COINS]
    data = fetch_price_json(list_id)

    if not data:
        return None
    
    snapshot = []
    for coin_id in list_id:
        coin_data = data.get(coin_id)
        if not coin_data:
            return None
        price_usd = coin_data.get("usd")
        market_cap_usd = coin_data.get("usd_market_cap")
        change_24h_usd = coin_data.get("usd_24h_change")

        if not price_usd or not market_cap_usd or change_24h_usd is None:
            return None
        
        coin = next((coin for coin in TRACKED_COINS if coin_id == coin["id"]), None)
        
        snapshot.append({
            "id": coin_id,
            "name": coin["name"],
            "symbol": coin["symbol"],
            "price_usd": price_usd,
            "market_cap_usd": market_cap_usd,
            "change_24h": change_24h_usd
        })

    return snapshot


def get_top_movers():
    headers = {
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }
    params = {
        "vs_currency": "usd"
    }
    try:
        http_response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params=params,
            headers=headers,
            timeout=10)
        if not http_response.ok:
            return None
        
        data = http_response.json()

    except (requests.RequestException, ValueError):
        return None
    
    valid_coins = [
        coin
        for coin in data
        if coin["price_change_percentage_24h"] is not None
    ]
    gainers = sorted(
        valid_coins,
        key=lambda coin: coin["price_change_percentage_24h"],
        reverse=True
    )[:5]
    losers = sorted(
        valid_coins,
        key=lambda coin: coin["price_change_percentage_24h"]
    )[:5]

    gainers_list = []
    for coin_data in gainers:
        gainers_list.append({
            "id": coin_data["id"],
            "name": coin_data["name"],
            "symbol": coin_data["symbol"],
            "price_usd": coin_data["current_price"],
            "change_24h": coin_data["price_change_percentage_24h"]
        })

    losers_list = []
    for coin_data in losers:
        losers_list.append({
            "id": coin_data["id"],
            "name": coin_data["name"],
            "symbol": coin_data["symbol"],
            "price_usd": coin_data["current_price"],
            "change_24h": coin_data["price_change_percentage_24h"]
        })

    return {
        "gainers": gainers_list,
        "losers": losers_list
    }

def get_global_market():
    headers = {
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }
    try:
        http_response = requests.get(
            "https://api.coingecko.com/api/v3/global",
            headers=headers,
            timeout=10)
        
        if not http_response.ok:
            return None
        
        data = http_response.json()
        if not data["data"]:
            return None
        
        total_market_cap_usd = data.get("data", None).get("total_market_cap", None).get("usd", None)
        change_24h = data.get("data", None).get("market_cap_change_percentage_24h_usd", None)
        if total_market_cap_usd is None or change_24h is None:
            return None
        
        return {
            "total_market_cap_usd": format_market_cap(total_market_cap_usd),
            "change_24h": change_24h
        }
    except (requests.RequestException, ValueError):
        return None

def format_market_cap(value):
    if value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    elif value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    else:
        return f"{value:.0f}"
    
if __name__ == "__main__":
    # print("--- single coin ---")
    # print(get_coin_data("bitcoin"))

    # print("--- market snapshot ---")
    # print(get_market_snapshot())

    # print("--- top movers ---")
    # movers = get_top_movers()
    # if movers:
    #     print("Gainers:", movers["gainers"][:2])  # first 2 only
    #     print("Losers:", movers["losers"][:2])

    print("--- global market ---")
    print(get_global_market())
