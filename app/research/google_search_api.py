import os
import requests
from dotenv import load_dotenv

load_dotenv()
SEARCH_API_KEY = os.getenv('SEARCH_API_KEY')
SEARCH_CX = "763b0355752d042d1" #japan

def google_search_api(searchword, max_results=10):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": searchword,
        "key": SEARCH_API_KEY,
        "cx": SEARCH_CX,
        "num": max_results  # 1〜10件まで指定可能
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # ステータスコードがエラーのとき例外を発生

        data = response.json()
        items = data.get("items", [])

        if not items:
            return []

        results = [{"title": item.get("title"), "link": item.get("link")} for item in items]
        return results

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return []
    
def google_search_api_with_keyword(searchword, keyword, max_results=10):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": searchword,
        "key": SEARCH_API_KEY,
        "cx": SEARCH_CX,
        "num": max_results  # 1〜10件まで指定可能
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # ステータスコードがエラーのとき例外を発生

        data = response.json()
        items = data.get("items", [])

        if not items:
            return []

        results = [{"title": item.get("title"), "link": item.get("link")} for item in items]
        for result in results:
            if keyword.lower() in result["title"].lower():
                return result["link"]
        return None

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None

if __name__ == "__main__":
    result = google_search_api('りんご', max_results=10)
    print(result[0]['link'])
