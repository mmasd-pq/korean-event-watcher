import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
import logging

class EventFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.logger = logging.getLogger(__name__)
    
    def fetch_events_from_site(self, site_config: Dict) -> List[Dict]:
        """指定サイトからイベント情報を取得"""
        try:
            self.logger.info(f"Fetching events from {site_config['name']}")
            
            response = self.session.get(site_config['url'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            events = []
            
            # セレクタに基づいてイベント要素を取得
            event_elements = soup.select(site_config['selector'])
            
            for element in event_elements:
                event = self.extract_event_data(element, site_config['name'])
                if event:
                    events.append(event)
            
            self.logger.info(f"Found {len(events)} events from {site_config['name']}")
            return events
            
        except Exception as e:
            self.logger.error(f"Error fetching from {site_config['name']}: {e}")
            return []
    
    def extract_event_data(self, element, site_name: str) -> Optional[Dict]:
        """HTML要素からイベントデータを抽出"""
        try:
            title_elem = element.select_one('h3, .title, .event-title, [class*="title"]')
            title = title_elem.get_text(strip=True) if title_elem else "No Title"
            
            content_elem = element.select_one('p, .content, .description, [class*="desc"]')
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            link_elem = element.select_one('a')
            event_url = link_elem.get('href') if link_elem else ""
            
            # 相対URLを絶対URLに変換
            if event_url and not event_url.startswith('http'):
                base_urls = {
                    '현대백화점': 'https://www.ehyundai.com',
                    'ロッテ百貨店': 'https://www.lotteshopping.com',
                    'BT21 SHOP': 'https://bt21.com',
                    'HYBE Insight': 'https://hybecorp.com'
                }
                base_url = base_urls.get(site_name, '')
                if base_url:
                    event_url = base_url + event_url
            
            return {
                'site_name': site_name,
                'title': title,
                'content': content,
                'url': event_url
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting event data: {e}")
            return None
    
    def fetch_all_events(self, target_urls: List[Dict]) -> List[Dict]:
        """全サイトからイベントを取得"""
        all_events = []
        
        for site_config in target_urls:
            events = self.fetch_events_from_site(site_config)
            all_events.extend(events)
            
            # サイト間で少し間隔を空ける
            time.sleep(1)
        
        return all_events


