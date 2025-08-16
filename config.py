# config.py - 修正完全版
import os

# === API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# === Database ===
DB_PATH = "data/events.db"

# === 実行間隔設定 (main.pyで必要) ===
CHECK_INTERVAL = 7200  # 2時間 = 7200秒

# === Scraping Settings ===
DEFAULT_DELAY = 2.0  # サイト間の待機時間（秒）
REQUEST_TIMEOUT = 15
MAX_RETRIES = 3

# === User Agent設定 ===
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# === Target URLs (修正版) ===
TARGET_URLS = [
    # --- 映画館 ---
    {
        "name": "MEGABOX イベント",
        "url": "https://www.megabox.co.kr/event",
        "selector": "a[href*='/event/'], .event a, .list a",
        "base_url": "https://www.megabox.co.kr",
        "max_items": 20,
        "delay": 3.0,
        "requires_js": False,
        "enabled": True
    },
    {
        "name": "CGV イベント", 
        "url": "https://www.cgv.co.kr/culture-event/event/",
        "selector": ".event-list a, .list a, a[href*='/event/']",
        "base_url": "https://www.cgv.co.kr", 
        "max_items": 10,
        "delay": 3.0,
        "requires_js": True,
        "enabled": False  # JavaScript必須のため一旦無効化
    },
    {
        "name": "LOTTE CINEMA イベント",
        "url": "https://www.lottecinema.co.kr/LCWS/Event/EventList.aspx",
        "selector": ".event-item a, .list a, a[href*='/Event/']",
        "base_url": "https://www.lottecinema.co.kr",
        "max_items": 10, 
        "delay": 3.0,
        "requires_js": True,
        "enabled": False  # JavaScript必須のため一旦無効化
    },

    # --- K-POP/エンタメ系 ---
    {
        "name": "HYBE Press（英語）",
        "url": "https://hybecorp.com/eng/news/news",
        "selector": ".news_list li a, .list li a, a[href*='/eng/news/news/']",
        "base_url": "https://hybecorp.com",
        "max_items": 30,
        "delay": 2.0,
        "enabled": True
    },
    {
        "name": "HYBE Notice（英語）", 
        "url": "https://hybecorp.com/eng/news/notice",
        "selector": ".news_list li a, .list li a, a[href*='/eng/news/notice/']",
        "base_url": "https://hybecorp.com",
        "max_items": 30,
        "delay": 2.0,
        "enabled": True
    },
    {
        "name": "YG Entertainment NOTICE（英語）",
        "url": "https://ygfamily.com/en/news/notice", 
        "selector": ".board-list a, .notice-list a, a[href*='/en/news/notice/']",
        "base_url": "https://ygfamily.com",
        "max_items": 20,
        "delay": 2.0,
        "enabled": True
    },

    # --- キャラクター系 ---
    {
        "name": "Pokemon Korea ニュース",
        "url": "https://pokemonkorea.co.kr/news",
        "selector": ".news-list a, .news_item a, a[href*='/news/']",
        "base_url": "https://pokemonkorea.co.kr",
        "max_items": 15,
        "delay": 2.0,
        "enabled": True
    },
    {
        "name": "BT21 公式 NOTICE",
        "url": "https://www.bt21.com/notice",
        "selector": ".notice a, .list a, a[href*='/notice']",
        "base_url": "https://www.bt21.com", 
        "max_items": 15,
        "delay": 2.0,
        "enabled": True
    },
    {
        "name": "LINE FRIENDS SQUARE（イベント系ブログ）",
        "url": "https://linefriendssquare.com/en/blogs/event",
        "selector": "article a, .card a, a[href*='/blogs/event/']",
        "base_url": "https://linefriendssquare.com",
        "max_items": 20,
        "delay": 2.0,
        "enabled": True
    },

    # --- 大型モール ---
    {
        "name": "IFC Mall Seoul - NOW（英語）",
        "url": "https://www.ifcmallseoul.com/eng/now",
        "selector": "a[href*='/now/'], .now a, .list a",
        "base_url": "https://www.ifcmallseoul.com",
        "max_items": 25,
        "delay": 2.0,
        "enabled": True
    },

    # --- 観光・公式サイト ---
    {
        "name": "VisitSeoul - Festivals & Events（英語）",
        "url": "https://english.visitseoul.net/events",
        "selector": ".event_list a, .list a, a[href*='/events/']",
        "base_url": "https://english.visitseoul.net",
        "max_items": 15,
        "delay": 2.0,
        "enabled": True
    },
    {
        "name": "韓国観光公社 イベント",
        "url": "https://korean.visitkorea.or.kr/list/fes_list.do",
        "selector": ".event a, .list a, a[href*='event']",
        "base_url": "https://korean.visitkorea.or.kr",
        "max_items": 15, 
        "delay": 2.0,
        "enabled": True
    },

    # --- 検索エンジン活用 ---
    {
        "name": "NAVER 検索：팝업스토어", 
        "url": "https://search.naver.com/search.naver?query=%ED%8C%9D%EC%97%85%EC%8A%A4%ED%86%A0%EC%96%B4",
        "selector": ".news_tit, .api_txt_lines, a[href*='blog'], a[href*='news']",
        "base_url": "https://search.naver.com",
        "max_items": 20,
        "link_must_include": ["팝업","popup"],
        "delay": 3.0,
        "enabled": True
    },

    # --- 百貨店系（追加） ---
    {
        "name": "롯데백화점 이벤트",
        "url": "https://www.lotteshopping.com/event/eventList",
        "selector": ".event-item a, .list a, a[href*='/event/']",
        "base_url": "https://www.lotteshopping.com",
        "max_items": 20,
        "delay": 3.0,
        "enabled": True
    },
    {
        "name": "신세계백화점 이벤트",
        "url": "https://www.shinsegae.com/event/list.do",
        "selector": ".event a, .list a, a[href*='/event/']",
        "base_url": "https://www.shinsegae.com",
        "max_items": 20,
        "delay": 3.0,
        "enabled": True
    }
]

# 有効なサイトのみをフィルター
TARGET_URLS = [site for site in TARGET_URLS if site.get("enabled", True)]

# === フィルター設定 ===
FILTER_KEYWORDS = [
    # 限定・希少
    "한정","限定","limited","exclusive",
    "선착","先착","first come",
    "단독","独占","only",
    "수량한정","数量限定","limited quantity",
    "기간한정","期間限定","limited time",

    # ポップアップ/コラボ
    "팝업","ポップアップ","popup","pop-up",
    "팝업스토어","ポップアップストア","popup store",
    "콜라보","コラボ","collaboration","collab",
    "특별","特別","special",

    # K-POP/グッズ
    "콘서트","コンサート","concert",
    "팬미팅","ファンミーティング","fanmeeting","fan meeting",
    "사인회","サイン会","signing","autograph",
    "굿즈","グッズ","merch","goods","merchandise",
    "앨범","アルバム","album",
    "포토카드","フォトカード","photocard","pc",

    # キャラクター系
    "포켓몬","ポケモン","pokemon","피카츄","ピカチュウ","pikachu",
    "bt21","라인프렌즈","line friends","카카오프렌즈","kakao friends",
    "산리오","サンリオ","sanrio","hello kitty","헬로키티",

    # 販売・イベント
    "이벤트","event","특가","sale","할인","discount",
    "신제품","new","launch","런칭","출시",
    "선물","プレゼント","gift","present",
    "추첨","抽選","lottery","응모","応募",

    # 期間・数量
    "조기마감","早期終了","early bird",
    "당일","当日","today only",
    "주말","週末","weekend",
    "예약","予約","reservation","booking",

    # ブランド系
    "bts","방탄소년단","블랙핑크","blackpink","아이브","ive",
    "뉴진스","newjeans","르세라핌","le sserafim"
]

# === 除外キーワード（ノイズ除去用） ===
EXCLUDE_KEYWORDS = [
    "광고","advertisement","ad",
    "스팸","spam",
    "성인","adult","19+",
    "도박","gambling","베팅","betting"
]

# === 通知設定 ===
NOTIFICATION_ENABLED = True
SLACK_ENABLED = bool(SLACK_WEBHOOK_URL and SLACK_WEBHOOK_URL != "")
PRINT_ENABLED = True

# === ChatGPT API設定 ===
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = 500
OPENAI_TEMPERATURE = 0.3

# === ログ設定 ===
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "logs/korean_event_watcher.log"

# === その他の設定 ===
# データベース関連
DB_BACKUP_DAYS = 30  # 30日以上古いデータは削除
MAX_DB_SIZE_MB = 100  # DBサイズ上限

# スクレイピング関連
CONCURRENT_REQUESTS = 3  # 同時リクエスト数
RETRY_DELAY = 5  # リトライ間隔（秒）

# 翻訳関連
TRANSLATE_TO_JAPANESE = True
SUMMARIZE_CONTENT = True
MAX_SUMMARY_LENGTH = 200  # 要約の最大文字数

