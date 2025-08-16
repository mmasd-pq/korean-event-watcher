import os
from dotenv import load_dotenv

load_dotenv()

# 監視対象URL群（韓国の百貨店・キャラクターショップ・K-POP公式サイト）
TARGET_URLS = [
    # 百貨店・ショッピングモール
    {
        "name": "현대백화점 (現代百貨店)",
        "url": "https://www.ehyundai.com/newPortal/DP/DPHP004_V.do",
        "selector": ".event-list .event-item"
    },
    {
        "name": "롯데백화점 (ロッテ百貨店)",
        "url": "https://www.lotteshopping.com/event/list",
        "selector": ".event-card"
    },
    {
        "name": "신세계백화점 (新世界百貨店)",
        "url": "https://www.shinsegae.com/event/list",
        "selector": ".event-item"
    },
    
    # ポップアップ専門・イベントスペース
    {
        "name": "더현대 서울 (The Hyundai Seoul)",
        "url": "https://www.thehyundai.com/event/popup",
        "selector": ".popup-event"
    },
    {
        "name": "성수동 팝업스토어",
        "url": "https://seongsu-popup.com/events",
        "selector": ".popup-list"
    },
    {
        "name": "홍대 팝업스트리트",
        "url": "https://hongdae-popup.com/store-list",
        "selector": ".store-item"
    },
    
    # K-POP・エンタメ関連
    {
        "name": "하이브 인사이트 (HYBE Insight)",
        "url": "https://hybecorp.com/event",
        "selector": ".event-content"
    },
    {
        "name": "SM 타운 (SM Town)",
        "url": "https://smtown.com/event/popup",
        "selector": ".popup-event"
    },
    {
        "name": "JYP 스토어 (JYP Store)",
        "url": "https://jypstore.com/popup",
        "selector": ".event-section"
    },
    {
        "name": "YG 엔터테인먼트 (YG Entertainment)",
        "url": "https://www.ygfamily.com/event/list",
        "selector": ".yg-event"
    },
    {
        "name": "YG 셀렉트 (YG SELECT)",
        "url": "https://ygselect.com/kr/event",
        "selector": ".select-event"
    },
    
    # キャラクター・ブランド
    {
        "name": "BT21 공식스토어",
        "url": "https://bt21.com/event",
        "selector": ".event-section"
    },
    {
        "name": "라인프렌즈 (LINE Friends)",
        "url": "https://linefriends.com/kr/event/popup",
        "selector": ".popup-item"
    },
    {
        "name": "카카오프렌즈 (Kakao Friends)",
        "url": "https://kakaofriends.com/kr/event",
        "selector": ".event-card"
    },
    # ポケモン関連サイト
    {
        "name": "포켓몬 코리아 공식 (Pokemon Korea Official)",
        "url": "https://pokemonkorea.co.kr/news/event",
        "selector": ".event-list .event-item"
    },
    {
        "name": "포켓몬 카드 게임 (Pokemon TCG Korea)",
        "url": "https://pokemon-tcg.co.kr/news",
        "selector": ".news-item"
    },
    {
        "name": "포켓몬 GO 코리아",
        "url": "https://pokemongo.co.kr/event",
        "selector": ".event-content"
    },
    {
        "name": "포켓몬 센터 온라인",
        "url": "https://pokemoncenter-online.com/kr/event",
        "selector": ".center-event"
    },
    
    # サンリオ関連サイト
    {
        "name": "산리오 코리아 공식 (Sanrio Korea Official)",
        "url": "https://sanrio.co.kr/event",
        "selector": ".sanrio-event"
    },
    {
        "name": "헬로키티 코리아 (Hello Kitty Korea)",
        "url": "https://hellokitty.co.kr/event/special",
        "selector": ".kitty-special"
    },
    {
        "name": "마이멜로디 코리아",
        "url": "https://mymelody.co.kr/news/event",
        "selector": ".melody-event"
    },
    {
        "name": "시나모롤 코리아 (Cinnamoroll Korea)",
        "url": "https://cinnamoroll.co.kr/event",
        "selector": ".cinnamon-event"
    },
    {
        "name": "구데타마 코리아 (Gudetama Korea)",
        "url": "https://gudetama.co.kr/special",
        "selector": ".gudetama-special"
    },
    
    # オンラインショッピング・イベント情報系
    {
        "name": "11번가 팝업",
        "url": "https://www.11st.co.kr/event/popup",
        "selector": ".popup-list"
    },
    {
        "name": "쿠팡 이벤트",
        "url": "https://www.coupang.com/np/campaigns/popup",
        "selector": ".event-item"
    },
    {
        "name": "롯데시네마 (LOTTE CINEMA)",
        "url": "https://www.lottecinema.co.kr/LCWS/Event/EventList.aspx",
        "selector": ".event-item"
    },
    {
        "name": "CGV 시네마",
        "url": "https://www.cgv.co.kr/culture-event/event/",
        "selector": ".event-list-item"
    },
    {
        "name": "메가박스 (MEGABOX)",
        "url": "https://www.megabox.co.kr/event",
        "selector": ".event-box"
    },
]

# 注目ワード
FILTER_KEYWORDS = [
    # 限定・イベント・エンタメ・グッズ・KPOP・キャラ・ポケモン・セール…（略）
    # ここは省略可能なら言ってください。全文のまま必要ならもう1回出します
]

# API設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# DBと実行インターバル
DB_PATH = "korea_events.db"
CHECK_INTERVAL = 7200  # 2時間
