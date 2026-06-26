import os
from dotenv import load_dotenv
import requests

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_crypto_headlines():
    headers = {
        "X-Api-Key": NEWS_API_KEY 
    }

    params = {
        "q": 'bitcoin OR ethereum OR cryptocurrency OR crypto OR altcoin OR "crypto ETF"',
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20
    }

    try:
        http_response = requests.get(
            "https://newsapi.org/v2/everything",
            params=params,
            headers=headers,
            timeout=10)
        
        if not http_response.ok:
            return None
        
        data = http_response.json()

        articles = []
        for article in data["articles"]:
            source = article.get("source", {}).get("name")
            title = article.get("title")
            description = article.get("description")
            url = article.get("url")
            published_at = article.get("publishedAt")

            if title is None and url is None or title == "[Removed]":
                continue
            articles.append({
                "source": source,
                "title": title,
                "description": description,
                "url": url,
                "published_at": published_at
            })

        return articles
    except (requests.RequestException, ValueError, KeyError):
        return None

if __name__ == "__main__":
    print(get_crypto_headlines())