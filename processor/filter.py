# processor/filter.py
import logging
import unicodedata
from typing import List, Dict

logger = logging.getLogger(__name__)

def _normalize(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s).lower().strip()
    s = " ".join(s.split())
    return s

class EventFilter:
    def __init__(self, keywords: List[str]):
        self.keywords = [_normalize(k) for k in keywords if k]

    def is_interesting(self, event: Dict) -> bool:
        title = _normalize(event.get("title", ""))
        content = _normalize(event.get("content", ""))
        text = f"{title} {content}".strip()

        for kw in self.keywords:
            if kw and kw in text:
                logger.debug(f"[HIT] kw='{kw}' title='{event.get('title','')[:60]}'")
                return True
        return False

    def filter_events(self, events: List[Dict]) -> List[Dict]:
        hits = [e for e in events if self.is_interesting(e)]
        logger.info(f"Filtered {len(hits)} interesting events from {len(events)} total events")
        return hits
