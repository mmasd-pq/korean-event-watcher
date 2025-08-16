
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
    
    # 온라인 쇼핑몰・이벤트 정보 사이트
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

# 注目ワード（韓国語＋日本語＋英語）
FILTER_KEYWORDS = [
    # 限定性・希少性
    "한정", "限定", "limited", "exclusive",
    "선착순", "先着", "first come", "선착",
    "단독", "独占", "only", "exclusive",
    "완전한정", "完全限定",
    
    # イベント・エンタメ
    "콘서트", "コンサート", "concert",
    "팬미팅", "ファンミーティング", "fanmeeting", "fan meeting",
    "사인회", "サイン会", "signing event",
    "굿즈", "グッズ", "goods", "merchandise",
    "앨범", "アルバム", "album",
    "포토카드", "フォトカード", "photocard",
    
    # ポップアップ関連キーワード（강화）
    "팝업", "ポップアップ", "popup", "pop-up", "pop up",
    "팝업스토어", "ポップアップストア", "popup store",
    "임시매장", "臨時店舗", "temporary store",
    "기간한정매장", "期間限定店舗", "limited time store",
    "체험존", "体験ゾーン", "experience zone",
    "콜라보", "コラボ", "collaboration", "collab",
    "한정오픈", "限定オープン", "limited opening",
    "특가", "特価", "special price",
    "세일", "セール", "sale", "할인",
    "신상", "新商品", "new product", "신제품",
    "런칭", "ランチング", "launching", "launch",
    "오픈", "オープン", "open", "grand open",
    
    # K-POP・キャラクター関連
    "bts", "방탄", "バンタン",
    "blackpink", "블랙핑크",
    "twice", "트와이스",
    "stray kids", "스트레이키즈",
    "bt21", "라인프렌즈", "line friends",
    "카카오", "kakao", "카카오프렌즈",
    # サンリオキャラクター関連
    "산리오", "sanrio", "헬로키티", "hello kitty",
    "마이멜로디", "マイメロディ", "my melody",
    "시나모롤", "シナモロール", "cinnamoroll",
    "구데타마", "ぐでたま", "gudetama",
    "쿠로미", "クロミ", "kuromi",
    "폼폼푸린", "ポムポムプリン", "pompompurin",
    "케로피", "けろっぴ", "keroppi",
    "릴라쿠마", "リラックマ", "rilakkuma",
    "산리오 굿즈", "サンリオグッズ", "sanrio goods",
    "산리오 콜라보", "サンリオコラボ", "sanrio collab",
    
    # ポケモン関連
    "포켓몬", "ポケモン", "pokemon", "포켓몬스터",
    "피카츄", "ピカチュウ", "pikachu",
    "포켓몬카드", "ポケモンカード", "pokemon card", "포켓몬 tcg",
    "포켓몬센터", "ポケモンセンター", "pokemon center",
    "포켓몬스토어", "ポケモンストア", "pokemon store",
    "포켓몬 굿즈", "ポケモングッズ", "pokemon goods",
    "포켓몬 인형", "ポケモンぬいぐるみ", "pokemon plush",
    "포켓몬볼", "モンスターボール", "pokeball", "poke ball",
    "포켓몬 한정", "ポケモン限定", "pokemon limited",
    "포켓몬 콜라보", "ポケモンコラボ", "pokemon collab",
    
    # 数量・時間限定
    "수량한정", "数量限定", "quantity limited",
    "기간한정", "期間限定", "time limited",
    "당일한정", "当日限定", "today only",
    "조기마감", "早期終了", "while supplies last",
    
    # 価格・セール関連
    "반값", "半額", "50% off",
    "무료", "無料", "free",
    "증정", "プレゼント", "gift", "present",
    "경품", "景品", "prize",
    "추첨", "抽選", "lottery", "raffle",
    
    # 百貨店・ショップ限定
    "백화점", "百貨店", "department store",
    "매장", "店舗", "store only",
    "온라인", "オンライン", "online only",
    "오프라인", "オフライン", "offline only"
]

# API設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# データベース設定
DB_PATH = "korea_events.db"

# 実行間隔（秒）
CHECK_INTERVAL = 7200  # 2時間