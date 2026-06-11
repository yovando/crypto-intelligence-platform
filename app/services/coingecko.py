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

def get_market_snapshot(TRACKED_COINS):
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
        snapshot.append({
            "id": coin_id,
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
            print('here???')
            return None
        
        data = http_response.json()

    except (requests.RequestException, ValueError):
        print('here')
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
    loosers = sorted(
        valid_coins,
        key=lambda coin: coin["price_change_percentage_24h"]
    )[:5]
    print(gainers)
    print(loosers)

if __name__ == "__main__":
    # print(get_coin_data("bitcoin"))      # expect full dict
    # print(get_coin_data("not_acoin"))    # expect None
    # print(get_coin_data(""))             # expect None
    get_top_movers()
