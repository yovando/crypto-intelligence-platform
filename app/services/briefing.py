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
    
    snapshot_data = get_market_snapshot() or []
    global_data = get_global_market()
    fg_raw = get_fear_greed()
    news = get_balanced_news() or []

    snapshot_data = [c for c in snapshot_data if c["id"] in TRACKED_COINS]
    fg = None
    if fg_raw:
        fg = {
            "value": fg["value"],
            "classification": fg["classification"]
        }
    top_news = []
    if news:
        for article in news[:8]:
            top_news.append({
                "title": article["title"],
                "source": article["source"],
                "category": article["category"]
            })
    
    return {
        "snapshot_data": snapshot_data,
        "global_data": global_data,
        "fg": fg,
        "news": top_news,
    }

def generate_morning_brief():
    ctx = collect_briefing_context()
    if not ctx.get("snapshot_data") and not ctx.get("fg"):
        return None
    
    prompt = build_briefing_prompt(ctx)
    if not OPENAI_API_KEY:
        return None
    
    system_message = """
    You are a crypto market intelligence analyst.
    Write a concise morning briefing (3–4 short paragraphs).
    Explain: what happened, why it matters, what to watch next.
    Do not give financial advice or buy/sell recommendations.
    Tone: professional, clear, accessible."""

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
                                                
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return None

def build_briefing_prompt(context: dict):
    snapshot_lines = []
    for coin in context["snapshot_data"]:
        snapshot_lines.append(
            f"- {coin["id"]}: "
            f"${coin["price_usd"]:,.2f}, "
            f"Market Cap ${coin["market_cap_usd"]:,.0f}, "
            f"24h {coin["change_24h"]:+.2f}%"
        )
    
    news_lines = []
    for article in context["news"]:
        news_lines.append(
            f"- ({article['category']}) {article['title']} [{article['source']}]"
        )
    
    fg = context["fg"]

    return f"""
        Write today's crypto morning briefing.

        Market Snapshot:
        {chr(10).join(snapshot_lines)}

        Global Market:
        {context["global_data"]}

        Fear & Greed Index:
        Value: {fg["value"]}
        Classification: {fg["classification"]}

        Top News:
        {chr(10).join(news_lines)}

        Instructions:
        - Start with a one-sentence market overview.
        - Summarize the key market movements.
        - Mention important crypto and macro news.
        - Explain how sentiment (Fear & Greed) relates to the market.
        - Use 3-5 short paragraphs.
        - Do not make investment recommendations.
        - Do not invent facts.
        """

if __name__ == "__main__":
    # import json
    # ctx = collect_briefing_context()
    # print(json.dumps(ctx, indent=2, default=str))
    print(generate_morning_brief())
    