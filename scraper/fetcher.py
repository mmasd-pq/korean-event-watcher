import logging
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class EventFetcher:
    """
    config.TARGET_URLS にある {name, url, selector, [base_url]} を使って
    各サイトからイベント情報を取得するクラス。
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        })
        self.logger = logging.getLogger(__name__)

    def fetch_all_events(self, target_urls: List[Dict]) -> List[Dict]:
        """全ターゲットからイベントを取得し、フラットなリストにして返す"""
        all_events: List[Dict] = []
        for site in target_urls:
            events = self.fetch_events_from_site(site)
            all_events.extend(events)
            time.sleep(1)  # サイトへの負荷軽減
        return all_events

    def fetch_events_from_site(self, site: Dict) -> List[Dict]:
        """
        単一サイトからイベントを取得。
        site: {"name": str, "url": str, "selector": str, "base_url": str(任意)}
        """
        name = site["name"]
        url = site["url"]
        selector = site["selector"]
        base_url = site.get("base_url")  # 無くてもOK

        try:
            self.logger.info(f"Fetching: {name} - {url}")
            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            elements = soup.select(selector)

            results: List[Dict] = []
            for el in elements:
                item = self.extract_event_data(el, site, page_url=resp.url, base_url=base_url)
                if item:
                    results.append(item)

            self.logger.info(f"{name}: {len(results)} events found")
            return results

        except Exception as e:
            self.logger.error(f"[{name}] fetch error: {e}")
            return []

    def extract_event_data(
        self, el, site: Dict, page_url: str, base_url: Optional[str] = None
    ) -> Optional[Dict]:
        """
        要素から title/content/url を抽出。
        相対リンクは base_url or page_url を基準に絶対URL化。
        """
        try:
            # タイトル候補
            title_el = el.select_one("h1, h2, h3, .title, .event-title, [class*='title']")
            title = title_el.get_text(strip=True) if title_el else "No Title"

            # 本文候補
            content_el = el.select_one("p, .content, .description, [class*='desc']")
            content = content_el.get_text(strip=True) if content_el else ""

            # リンク
            link_el = el.select_one("a")
            href = link_el.get("href") if link_el else ""

            # 絶対URL化（base_url があれば優先、無ければ取得ページURLを基準に）
            if href:
                if base_url:
                    event_url = urljoin(base_url, href)
                else:
                    event_url = urljoin(page_url, href)
            else:
                event_url = ""

            return {
                "site_name": site["name"],
                "title": title,
                "content": content,
                "url": event_url,
            }

        except Exception as e:
            self.logger.error(f"[{site['name']}] extract error: {e}")
            return None

