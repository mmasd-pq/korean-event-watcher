# config.py  — 2025-08-16 確認版（実在URLに絞り込み）
import os
from dotenv import load_dotenv
load_dotenv()

# === 監視対象URL（まずは堅い面子に厳選） ===
TARGET_URLS = [
    # --- 映画館（イベント告知が安定して掲載される） ---
    {
        "name": "MEGABOX イベント",
        "url": "https://www.megabox.co.kr/event",
        # イベント一覧→各詳細へのリンクが <a href="/event/detail?...">
        "selector": "a[href*='/event/detail']",
        "base_url": "https://www.megabox.co.kr"
    },
    {
        "name": "CGV イベント",
        "url": "https://www.cgv.co.kr/culture-event/event/",
        # リストの HTML はたびたび変わるので a を広めに
        "selector": "a[href*='/culture-event/event/'], a[href*='detailViewUnited.aspx']",
        "base_url": "https://www.cgv.co.kr"
    },
    {
        "name": "LOTTE CINEMA イベント",
        "url": "https://www.lottecinema.co.kr/LCWS/Event/EventList.aspx",
        "selector": "a[href*='EventDetail'], .event-item a",
        "base_url": "https://www.lottecinema.co.kr"
    },

    # --- K-POP/事務所ニュース・お知らせ ---
    {
        "name": "HYBE Press（英語）",
        "url": "https://hybecorp.com/eng/news/news",
        "selector": ".news_list li a, .list li a, a[href*='/eng/news/news/']",
        "base_url": "https://hybecorp.com"
    },
    {
        "name": "HYBE Notice（英語）",
        "url": "https://hybecorp.com/eng/news/notice",
        "selector": ".news_list li a, .list li a, a[href*='/eng/news/notice/']",
        "base_url": "https://hybecorp.com"
    },
    {
        "name": "SM Entertainment NEWS",
        "url": "https://www.smentertainment.com/News",
        "selector": ".news_list li a, .list li a, a[href*='/News/']",
        "base_url": "https://www.smentertainment.com"
    },
    {
        "name": "YG Entertainment NOTICE（英語）",
        "url": "https://ygfamily.com/en/news/notice",
        "selector": ".board-list a, .notice-list a, a[href*='/en/news/notice/']",
        "base_url": "https://ygfamily.com"
    },

    # --- キャラクター/ポップアップ系（公式の告知面） ---
    {
        "name": "Pokemon Korea ニュース",
        "url": "https://pokemonkorea.co.kr/news",
        "selector": ".news-list a, .news_item a, a[href*='/news/']",
        "base_url": "https://pokemonkorea.co.kr"
    },
    {
        "name": "BT21 公式 NOTICE",
        "url": "https://www.bt21.com/notice",
        "selector": ".notice a, .list a, a[href*='/notice']",
        "base_url": "https://www.bt21.com"
    },
    {
        "name": "LINE FRIENDS SQUARE（イベント系ブログ）",
        "url": "https://linefriendssquare.com/en/blogs/event",
        "selector": "article a, .card a, a[href*='/blogs/event/']",
        "base_url": "https://linefriendssquare.com"
    },

    # --- 大型モール（“NOW/NEWS/WHAT’S ON”にイベント掲載） ---
    {
        "name": "IFC Mall Seoul - NOW（英語）",
        "url": "https://www.ifcmallseoul.com/eng/now",
        "selector": "a, .list a, .now a",
        "base_url": "https://www.ifcmallseoul.com"
    },

    # --- 公的ポータル（イベント集約・拾い漏れの保険） ---
    {
        "name": "VisitSeoul - Festivals & Events（英語）",
        "url": "https://english.visitseoul.net/events",
        "selector": ".event_list a, .list a, a[href*='/events/']",
        "base_url": "https://english.visitseoul.net"
    },

    # --- 横断検索（Naver 検索結果。HTML出力が安定しやすい） ---
    {
        "name": "NAVER 検索：팝업스토어",
        "url": "https://search.naver.com/search.naver?query=%ED%8C%9D%EC%97%85%EC%8A%A4%ED%86%A0%EC%96%B4",
        "selector": "a",
        "base_url": "https://search.naver.com",
        "max_items": 20,                         # ★ 上位20件に制限
        "link_must_include": ["팝업","popup"],   # ★ “팝업/popup” を含むリンク/テキストだけ通す

    },
]

# === 注目ワード ===
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
]

# API/通知
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# DB/実行間隔
DB_PATH = "korea_events.db"
CHECK_INTERVAL = 7200  # 2時間

