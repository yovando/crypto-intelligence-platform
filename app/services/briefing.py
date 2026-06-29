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
    
    
if __name__ == "__main__":
    print(test_openai_connection())