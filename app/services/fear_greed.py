import requests
from datetime import datetime
def get_fear_greed():
    params = {
        "limit": "7"
    }

    try:
        http_response = requests.get(
            "https://api.alternative.me/fng/",
            params=params,
            timeout=10)
        
        if not http_response.ok:
            return None
        
        data = http_response.json()

        if not data["data"]:
            return None

        history_fg = []
        for i, fg in enumerate(data["data"], start=1):
            if i == 1:
                current_fg = {
                    "value": int(fg["value"]),
                    "classification": fg["value_classification"],
                }
            
            if i > 1:
                history_fg.append({
                    "value": int(fg["value"]),
                    "classification": fg["value_classification"],
                    "date": datetime.fromtimestamp(int(fg["timestamp"])).strftime("%Y-%m-%d"),
                })

        return {
            "value": current_fg["value"],
            "classification": current_fg["classification"],
            "history": history_fg
        }
    except (requests.RequestException, ValueError):
        return None
    
    

if __name__ == "__main__":
    result = get_fear_greed()
    print(result)
    

    