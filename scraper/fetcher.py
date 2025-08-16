# scraper/fetcher.py - JavaScript対応改良版
import logging
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Selenium（オプション、JavaScript必須サイト用）
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class EventFetcher:
    """
    改良版EventFetcher - JavaScript動的サイト対応
    """

    def __init__(self, use_selenium=False, max_retries: int = 3):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        })
        self.logger = logging.getLogger(__name__)
        self.max_retries = max_retries
        self.use_selenium = use_selenium and SELENIUM_AVAILABLE
        
        if self.use_selenium:
            self._setup_selenium()

    def _setup_selenium(self):
        """Seleniumの設定"""
        try:
            self.chrome_options = Options()
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--no-sandbox')
            self.chrome_options.add_argument('--disable-dev-shm-usage')
            self.chrome_options.add_argument('--disable-gpu')
            self.chrome_options.add_argument('--window-size=1920,1080')
            self.logger.info("Selenium WebDriver configured")
        except Exception as e:
            self.logger.error(f"Selenium setup failed: {e}")
            self.use_selenium = False

    def fetch_all_events(self, target_urls: List[Dict]) -> List[Dict]:
        """全ターゲットからイベントを取得"""
        all_events: List[Dict] = []
        
        # 有効なサイトのみ処理
        valid_sites = [site for site in target_urls if site.get("enabled", True)]
        self.logger.info(f"Processing {len(valid_sites)} enabled sites")
        
        for site in valid_sites:
            try:
                # JavaScript必須サイトの処理
                if site.get("requires_js", False) and self.use_selenium:
                    events = self.fetch_events_with_selenium(site)
                else:
                    events = self.fetch_events_from_site(site)
                
                all_events.extend(events)
                
                # サイト別の待機時間
                delay = site.get('delay', 1.0)
                if delay > 0:
                    time.sleep(delay)
                    
            except Exception as e:
                self.logger.error(f"Unexpected error processing site {site['name']}: {e}")
                continue
        
        return all_events

    def fetch_events_with_selenium(self, site: Dict) -> List[Dict]:
        """Seleniumを使ってJavaScript動的サイトから取得"""
        if not self.use_selenium:
            self.logger.warning(f"Selenium not available for {site['name']}")
            return []

        name = site["name"]
        url = site["url"]
        selector = site["selector"]
        
        driver = None
        try:
            self.logger.info(f"Fetching with Selenium: {name} - {url}")
            
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.get(url)
            
            # ページの読み込みを待機
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)  # 追加の待機時間
            
            # HTMLを取得
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            
            elements = soup.select(selector)
            self.logger.info(f"{name}: Found {len(elements)} elements with Selenium")
            
            # フィルタリング処理
            base_url = site.get("base_url")
            max_items = site.get("max_items")
            must_include = site.get("link_must_include")

            if must_include:
                elements = self._filter_by_keywords(elements, must_include)
                self.logger.info(f"{name}: Filtered to {len(elements)} elements")

            if isinstance(max_items, int) and max_items > 0:
                elements = elements[:max_items]

            results: List[Dict] = []
            for el in elements:
                try:
                    item = self.extract_event_data(el, site, page_url=url, base_url=base_url)
                    if item:
                        results.append(item)
                except Exception as e:
                    self.logger.error(f"Error extracting data: {e}")
                    continue

            self.logger.info(f"{name}: {len(results)} events extracted with Selenium")
            return results

        except Exception as e:
            self.logger.error(f"[{name}] Selenium fetch error: {e}")
            return []
        finally:
            if driver:
                driver.quit()

    def fetch_events_from_site(self, site: Dict) -> List[Dict]:
        """通常のrequestsを使った取得（改良版）"""
        name = site["name"]
        url = site["url"]
        selector = site["selector"]
        base_url = site.get("base_url")
        max_items = site.get("max_items")
        must_include = site.get("link_must_include")

        try:
            self.logger.info(f"Fetching: {name} - {url}")
            resp = self._fetch_with_retry(url)
            
            if not resp:
                return []

            soup = BeautifulSoup(resp.text, "html.parser")
            elements = soup.select(selector)
            
            self.logger.info(f"{name}: Found {len(elements)} elements")
            
            # 空の場合は代替セレクターを試す
            if not elements and selector != "a":
                self.logger.warning(f"{name}: No elements found, trying fallback selector 'a'")
                elements = soup.select("a")
                self.logger.info(f"{name}: Fallback found {len(elements)} links")

            # フィルタリング処理
            if must_include:
                elements = self._filter_by_keywords(elements, must_include)
                self.logger.info(f"{name}: Filtered to {len(elements)} elements")

            if isinstance(max_items, int) and max_items > 0:
                elements = elements[:max_items]

            results: List[Dict] = []
            for el in elements:
                try:
                    item = self.extract_event_data(el, site, page_url=resp.url, base_url=base_url)
                    if item and self._is_valid_event(item):
                        results.append(item)
                except Exception as e:
                    self.logger.debug(f"Error extracting data from element: {e}")
                    continue

            self.logger.info(f"{name}: {len(results)} valid events extracted")
            return results

        except Exception as e:
            self.logger.error(f"[{name}] fetch error: {e}")
            return []

    def _fetch_with_retry(self, url: str) -> Optional[requests.Response]:
        """リトライ機能付きの取得"""
        for attempt in range(self.max_retries):
            try:
                resp = self.session.get(url, timeout=15)
                resp.raise_for_status()
                return resp
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数バックオフ
        return None

    def _filter_by_keywords(self, elements, keywords: List[str]):
        """キーワードによるフィルタリング"""
        filtered = []
        for el in elements:
            link_el = el if el.name == "a" else el.select_one("a")
            href = (link_el.get("href") if link_el else "") or ""
            text = (link_el.get_text(" ", strip=True) if link_el else el.get_text(" ", strip=True)) or ""
            
            combined = (href + " " + text).lower()
            if any(keyword.lower() in combined for keyword in keywords):
                filtered.append(el)
        return filtered

    def _is_valid_event(self, event: Dict) -> bool:
        """イベントデータの妥当性チェック"""
        # 最低限のバリデーション
        if not event.get("title") or event["title"] in ["No Title", ""]:
            return False
        
        # 無効なリンクをフィルタ
        url = event.get("url", "")
        if url.startswith("javascript:") or url.startswith("mailto:"):
            return False
        
        return True

    def extract_event_data(
        self, el, site: Dict, page_url: str, base_url: Optional[str] = None
    ) -> Optional[Dict]:
        """要素からイベントデータを抽出（改良版）"""
        try:
            # タイトル抽出の改良
            title = self._extract_title(el)
            if not title:
                return None

            # 内容抽出
            content = self._extract_content(el)

            # URL抽出と正規化
            event_url = self._extract_and_normalize_url(el, page_url, base_url)

            return {
                "site_name": site["name"],
                "title": title[:200],  # 長さ制限
                "content": content[:500] if content else "",
                "url": event_url,
                "fetched_at": time.time()
            }

        except Exception as e:
            self.logger.debug(f"Extract error for {site['name']}: {e}")
            return None

    def _extract_title(self, el) -> Optional[str]:
        """タイトル抽出"""
        # 優先順位付きのセレクター
        title_selectors = [
            "h1, h2, h3, h4",
            ".title, .headline, .subject",
            "[class*='title'], [class*='subject']",
            "strong, b",
            "a"
        ]
        
        for selector in title_selectors:
            title_el = el.select_one(selector)
            if title_el:
                title = title_el.get_text(strip=True)
                if title and len(title) > 2:  # 最低限の長さチェック
                    return title
        
        # 最後の手段：要素全体のテキスト
        full_text = el.get_text(strip=True)
        if full_text and len(full_text) > 2:
            # 最初の100文字を使用
            return full_text[:100].split('\n')[0].strip()
        
        return None

    def _extract_content(self, el) -> str:
        """内容抽出"""
        content_selectors = [
            "p, .content, .description, .summary",
            "[class*='desc'], [class*='content']"
        ]
        
        for selector in content_selectors:
            content_el = el.select_one(selector)
            if content_el:
                content = content_el.get_text(" ", strip=True)
                if content and len(content) > 5:
                    return content
        
        return ""

    def _extract_and_normalize_url(self, el, page_url: str, base_url: Optional[str]) -> str:
        """URL抽出と正規化"""
        link_el = el.select_one("a")
        if not link_el:
            return ""
        
        href = link_el.get("href", "").strip()
        if not href:
            return ""
        
        # JavaScriptリンクをスキップ
        if href.startswith("javascript:") or href.startswith("mailto:"):
            return ""
        
        try:
            # 絶対URL化
            if base_url:
                return urljoin(base_url, href)
            else:
                return urljoin(page_url, href)
        except:
            return ""

    def close(self):
        """リソースのクリーンアップ"""
        if hasattr(self, 'session'):
            self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 使用例とテスト関数
def test_fetcher():
    """テスト実行"""
    from config import TARGET_URLS
    
    # 基本テスト
    basic_fetcher = EventFetcher(use_selenium=False)
    
    # JavaScript対応テスト（Seleniumが利用可能な場合）
    if SELENIUM_AVAILABLE:
        selenium_fetcher = EventFetcher(use_selenium=True)
        print("✅ Selenium available")
    else:
        print("⚠️ Selenium not available")
    
    # 1つのサイトでテスト
    test_site = TARGET_URLS[0]  # MEGABOX
    events = basic_fetcher.fetch_events_from_site(test_site)
    print(f"Test result: {len(events)} events from {test_site['name']}")

if __name__ == "__main__":
    test_fetcher()
