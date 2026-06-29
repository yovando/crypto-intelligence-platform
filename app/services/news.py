import os
from dotenv import load_dotenv
import requests

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_crypto_headlines():
    return fetch_headlines(
        'bitcoin OR ethereum OR cryptocurrency OR crypto OR altcoin OR "crypto ETF"',
        "crypto")

def get_macro_headlines():
    return fetch_headlines(
        'inflation OR "interest rates" OR "federal reserve" OR CPI OR unemployment OR "nonfarm payrolls"',
        "macro")

def fetch_headlines(query: str, category: str):
    headers = {
        "X-Api-Key": NEWS_API_KEY 
    }

    params = {
        "q": query,
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
            image_url = article.get("urlToImage")

            if title is None or url is None or title == "[Removed]":
                continue
            articles.append({
                "source": source,
                "title": title,
                "description": description,
                "url": url,
                "image_url": image_url,
                "category": category,
                "published_at": published_at
            })

        return articles

    except (requests.RequestException, ValueError, KeyError):
        return None

# if __name__ == "__main__":
#     print(NEWS_API_KEY)
#     headlines = get_crypto_headlines()
#     print(headlines)