# config.py - 修正版
import os

# === API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# === Database ===
DB_PATH = "data/events.db"

# === Scraping Settings ===
DEFAULT_DELAY = 2.0  # サイト間の待機時間（秒）
REQUEST_TIMEOUT = 15
MAX_RETRIES = 3

# === Target URLs (修正版) ===
TARGET_URLS = [
    # --- 映画館 (問題があったので修正) ---
    {
        "name": "MEGABOX イベント",
        "url": "https://www.megabox.co.kr/event",
        # 修正: より広範囲でイベントリンクを捕捉
        "selector": "a[href*='/event/'], .event a, .list a",
        "base_url": "https://www.megabox.co.kr",
        "max_items": 20,
        "delay": 3.0,  # 少し長めの待機
        "requires_js": False
    },
    {
        "name": "CGV イベント", 
        "url": "https://www.cgv.co.kr/culture-event/event/",
        # JavaScript動的サイトのため、一旦無効化
        "selector": "a",
        "base_url": "https://www.cgv.co.kr", 
        "max_items": 10,
        "delay": 3.0,
        "requires_js": True,  # JavaScript必須フラグ
        "enabled": False      # 一旦無効化
    },
    {
        "name": "LOTTE CINEMA イベント",
        "url": "https://www.lottecinema.co.kr/LCWS/Event/EventList.aspx",
        "selector": "a",
        "base_url": "https://www.lottecinema.co.kr",
        "max_items": 10, 
        "delay": 3.0,
        "requires_js": True,
        "enabled": False      # 一旦無効化
    },

    # --- K-POP/事務所 (これらは動作していたので維持) ---
    {
        "name": "HYBE Press（英語）",
        "url": "https://hybecorp.com/eng/news/news",
        "selector": ".news_list li a, .list li a, a[href*='/eng/news/news/']",
        "base_url": "https://hybecorp.com",
        "max_items": 30,
        "delay": 2.0
    },
    {
        "name": "HYBE Notice（英語）", 
        "url": "https://hybecorp.com/eng/news/notice",
        "selector": ".news_list li a, .list li a, a[href*='/eng/news/notice/']",
        "base_url": "https://hybecorp.com",
        "max_items": 30,
        "delay": 2.0
    },
    # SM Entertainment は404エラーのため一旦コメントアウト
    # {
    #     "name": "SM Entertainment NEWS",
    #     "url": "https://www.smentertainment.com/News", 
    #     "selector": ".news_list li a, .list li a, a[href*='/News/']",
    #     "base_url": "https://www.smentertainment.com"
    # },
    {
        "name": "YG Entertainment NOTICE（英語）",
        "url": "https://ygfamily.com/en/news/notice", 
        "selector": ".board-list a, .notice-list a, a[href*='/en/news/notice/']",
        "base_url": "https://ygfamily.com",
        "max_items": 20,
        "delay": 2.0
    },

    # --- キャラクター系 ---
    {
        "name": "Pokemon Korea ニュース",
        "url": "https://pokemonkorea.co.kr/news",
        "selector": ".news-list a, .news_item a, a[href*='/news/'], a", # より広範囲に
        "base_url": "https://pokemonkorea.co.kr",
        "max_items": 15,
        "delay": 2.0
    },
    {
        "name": "BT21 公式 NOTICE",
        "url": "https://www.bt21.com/notice",
        "selector": ".notice a, .list a, a[href*='/notice'], a", # より広範囲に
        "base_url": "https://www.bt21.com", 
        "max_items": 15,
        "delay": 2.0
    },
    {
        "name": "LINE FRIENDS SQUARE（イベント系ブログ）",
        "url": "https://linefriendssquare.com/en/blogs/event",
        "selector": "article a, .card a, a[href*='/blogs/event/']",
        "base_url": "https://linefriendssquare.com",
        "max_items": 20,
        "delay": 2.0
    },

    # --- 大型モール ---
    {
        "name": "IFC Mall Seoul - NOW（英語）",
        "url": "https://www.ifcmallseoul.com/eng/now",
        "selector": "a, .list a, .now a",
        "base_url": "https://www.ifcmallseoul.com",
        "max_items": 50,  # 多めに取得していたので調整
        "delay": 2.0
    },

    # --- 公的ポータル ---
    {
        "name": "VisitSeoul - Festivals & Events（英語）",
        "url": "https://english.visitseoul.net/events",
        "selector": ".event_list a, .list a, a[href*='/events/']",
        "base_url": "https://english.visitseoul.net",
        "max_items": 15,
        "delay": 2.0
    },

    # --- 横断検索 (これは動作していた) ---
    {
        "name": "NAVER 検索：팝업스토어", 
        "url": "https://search.naver.com/search.naver?query=%ED%8C%9D%EC%97%85%EC%8A%A4%ED%86%A0%EC%96%B4",
        "selector": "a",
        "base_url": "https://search.naver.com",
        "max_items": 20,
        "link_must_include": ["팝업","popup"],
        "delay": 3.0  # NAVERは少し慎重に
    },

    # === 追加候補サイト ===
    {
        "name": "Seoul ポップアップストア情報",
        "url": "https://korean.visitseoul.net/things-to-do/popup-stores",
        "selector": "a[href*='popup'], .popup a, a",
        "base_url": "https://korean.visitseoul.net", 
        "max_items": 10,
        "delay": 2.0
    },
    {
        "name": "韓国観光公社 イベント",
        "url": "https://korean.visitkorea.or.kr/list/fes_list.do",
        "selector": ".event a, .list a, a[href*='event'], a",
        "base_url": "https://korean.visitkorea.or.kr",
        "max_items": 15, 
        "delay": 2.0
    }
]

# 有効なサイトのみをフィルター
TARGET_URLS = [site for site in TARGET_URLS if site.get("enabled", True)]

# === フィルター設定 ===
FILTER_KEYWORDS = [
    # 限定・希少
    "한정","限定","limited","exclusive",
    "선착","先着","first come",
    "단독","独占","only",

    # ポップアップ/コラボ
    "팝업","ポップアップ","popup","pop-up",
    "팝업스토어","ポップアップストア","popup store",
    "콜라보","コラボ","collaboration","collab",

    # K-POP/グッズ
    "콘서트","コンサート","concert",
    "팬미팅","ファンミーティング","fanmeeting",
    "사인회","サイン会","signing",
    "굿즈","グッズ","merch","goods",
    "앨범","アルバム","album",
    "포토카드","フォトカード","photocard",

    # ポケモン・キャラ
    "포켓몬","ポケモン","pokemon","피카츄","ピカチュウ",
    "bt21","라인프렌즈","line friends","카카오프렌즈","kakao friends",
    "산리오","サンリオ","sanrio",

    # 数量・期間
    "수량한정","数量限定","기간한정","期間限定","조기마감","早期終了",
    
    # 新規追加: より一般的なワード
    "이벤트","event","특가","sale","할인","discount","신제품","new"
]

# === 通知設定 ===
NOTIFICATION_ENABLED = True
SLACK_ENABLED = bool(SLACK_WEBHOOK_URL)
PRINT_ENABLED = True

# === ログ設定 ===
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

