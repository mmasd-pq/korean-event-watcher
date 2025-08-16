# processor/filter.py
import logging
import unicodedata
from typing import List, Dict

logger = logging.getLogger(__name__)

def _normalize(s: str) -> str:
    if not s:
        return ""
    # NFKCで幅や互換文字を正規化 → 小文字化 → 連続空白を1つに
    s = unicodedata.normalize("NFKC", s)
    s = s.lower().strip()
    s = " ".join(s.split())
    return s

def is_interesting(event: Dict, keywords: List[str]) -> bool:
    title = _normalize(event.get("title", ""))
    content = _normalize(event.get("content", ""))
    text = f"{title} {content}"

    for kw in keywords:
        nkw = _normalize(kw)
        if not nkw:
            continue
        if nkw in text:
            logger.debug(f"HIT: '{kw}' matched in '{event.get('title','')[:60]}'")
            return True
    return False

def filter_events(events: List[Dict], keywords: List[str]) -> List[Dict]:
    hit = [e for e in events if is_interesting(e, keywords)]
    logger.info(f"Filtered {len(hit)} interesting events from {len(events)} total events")
    return hit
