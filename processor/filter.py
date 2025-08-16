# =============================================================================
# processor/filter.py - 注目ワードを含むイベントのフィルタリング
# =============================================================================
from typing import List, Dict
import logging

class EventFilter:
    def __init__(self, filter_keywords: List[str]):
        self.filter_keywords = [keyword.lower() for keyword in filter_keywords]
        self.logger = logging.getLogger(__name__)
    
    def filter_events(self, events: List[Dict]) -> List[Dict]:
        """注目ワードを含むイベントのみを抽出"""
        filtered_events = []
        
        for event in events:
            if self.is_interesting_event(event):
                filtered_events.append(event)
        
        self.logger.info(f"Filtered {len(filtered_events)} interesting events from {len(events)} total events")
        return filtered_events
    
    def is_interesting_event(self, event: Dict) -> bool:
        """イベントが注目に値するかを判定"""
        title = event.get('title', '').lower()
        content = event.get('content', '').lower()
        combined_text = f"{title} {content}"
        
        for keyword in self.filter_keywords:
            if keyword in combined_text:
                self.logger.debug(f"Event matched keyword '{keyword}': {event.get('title', '')}")
                return True
        
        return False