import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from config import TARGET_URLS


def fetch_html(url: str) -> str:
    """指定されたURLからHTMLを取得する"""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return ""


def extract_items(html: str, selector: str) -> List[str]:
    """HTMLから指定のセレクタにマッチする要素を抽出し、テキストリストとして返す"""
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select(selector)
    return [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]


def fetch_all_targets() -> List[Dict]:
    """
    config.pyのTARGET_URLSを元に、全サイトのイベント情報を取得。
    各イベントに name, url, selector, items を含むdictを返す。
    """
    results = []
    for target in TARGET_URLS:
        print(f"[INFO] Fetching: {target['name']} - {target['url']}")
        html = fetch_html(target["url"])
        if not html:
            continue
        items = extract_items(html, target["selector"])
        results.append({
            "name": target["name"],
            "url": target["url"],
            "items": items,
        })
    return results
