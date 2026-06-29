import os
from dotenv import load_dotenv
from openai import OpenAI
from app.services.coingecko import get_market_snapshot, get_global_market
from app.services.fear_greed import get_fear_greed
from app.database.queries import get_balanced_news

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def test_openai_connection():
    if not OPENAI_API_KEY:
        return None
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a crypto market analyst"},
                {"role": "user", "content": "In one sentence, what is Bitcoin?"},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return None
    
def collect_briefing_context():
    TRACKED_COINS = {"bitcoin", "ethereum", "solana"}
    
    snapshot_data = get_market_snapshot()
    snapshot_data = [
        coin for coin in snapshot_data if coin["id"] in TRACKED_COINS
    ]
    
    global_data = get_global_market()
    fg = get_fear_greed()
    news = get_balanced_news()
    
    top_news = []
    for i in range(0, 8, 1):
        top_news.append({
            "title": news[i]["title"],
            "source": news[i]["source"],
            "category ": news[i]["category"]
        })
        

    return {
        "snapshot_data": snapshot_data,
        "global_data": global_data,
        "fg": fg,
        "news": top_news,
    }
    
if __name__ == "__main__":
    import json
    ctx = collect_briefing_context()
    print(json.dumps(ctx, indent=2, default=str))
    