# debug_scraper.py - デバッグ用スクレイピングスクリプト
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# あなたの config.py の設定を直接ここに含める
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
    }
]

def debug_site(site_config):
    """
    特定サイトのHTML構造を詳細に調査するデバッグ関数
    """
    name = site_config.get("name", "Unknown")
    url = site_config.get("url", "")
    selector = site_config.get("selector", "")
    
    print(f"\n{'='*60}")
    print(f"🔍 デバッグ中: {name}")
    print(f"URL: {url}")
    print(f"セレクター: {selector}")
    print(f"{'='*60}")
    
    if not url:
        print("❌ URLが設定されていません")
        return
    
    try:
        # HTML取得
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }
        
        print(f"📡 HTMLを取得中...")
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        print(f"✅ ステータス: {resp.status_code}")
        print(f"📄 HTMLサイズ: {len(resp.text)} 文字")
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # セレクターでの要素検索
        if selector:
            elements = soup.select(selector)
            print(f"🎯 セレクター '{selector}' で見つかった要素: {len(elements)}個")
            
            if elements:
                print(f"\n📝 最初の3要素の詳細:")
                for i, el in enumerate(elements[:3]):
                    print(f"\n--- 要素 {i+1} ---")
                    print(f"タグ名: {el.name}")
                    print(f"クラス: {el.get('class', [])}")
                    print(f"ID: {el.get('id', 'なし')}")
                    
                    # テキスト内容
                    text = el.get_text(strip=True)[:100]
                    print(f"テキスト: {text}...")
                    
                    # リンク
                    link = el.find("a")
                    if link:
                        href = link.get("href", "")
                        print(f"リンク: {href}")
                    else:
                        print("リンク: なし")
            else:
                # 代替セレクターを提案
                print(f"\n💡 代替セレクター候補:")
                suggest_selectors(soup)
        else:
            print("⚠️ セレクターが設定されていません")
            suggest_selectors(soup)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ リクエストエラー: {e}")
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")

def suggest_selectors(soup):
    """HTML構造を分析して適切なセレクターを提案"""
    suggestions = []
    
    # よくあるイベント系のセレクター候補
    candidates = [
        (".event", "イベント関連のクラス"),
        (".news", "ニュース関連のクラス"), 
        (".item", "アイテム系のクラス"),
        (".post", "投稿系のクラス"),
        (".article", "記事系のクラス"),
        ("article", "articleタグ"),
        (".list-item", "リストアイテム"),
        (".content-item", "コンテンツアイテム"),
        ("li", "リスト要素"),
        ("h2", "見出し2"),
        ("h3", "見出し3"),
    ]
    
    print("\n🔍 セレクター候補:")
    for selector, desc in candidates:
        elements = soup.select(selector)
        if elements:
            print(f"  {selector:15} → {len(elements):3d}個 ({desc})")
            
            # サンプルテキストを表示
            if elements[0]:
                sample_text = elements[0].get_text(strip=True)[:50]
                print(f"      例: {sample_text}...")

def debug_current_config():
    """現在の設定でデバッグを実行"""
    print(f"🎯 設定されているサイト数: {len(TARGET_URLS)}")
    
    # ユーザーに選択させる
    print("\n📋 デバッグしたいサイトを選択してください:")
    for i, site in enumerate(TARGET_URLS):
        name = site.get("name", f"サイト{i+1}")
        print(f"  {i+1}: {name}")
    
    print(f"  0: すべて")
    print(f"  99: 問題のあるサイトのみ（0件のサイト）")
    
    try:
        choice = input("\n番号を入力してください: ").strip()
        
        if choice == "0":
            for site in TARGET_URLS:
                debug_site(site)
        elif choice == "99":
            # 0件だったサイトのみをチェック
            problem_sites = [
                TARGET_URLS[0],  # MEGABOX
                TARGET_URLS[1],  # CGV  
                TARGET_URLS[2],  # LOTTE CINEMA
            ]
            for site in problem_sites:
                debug_site(site)
        else:
            idx = int(choice) - 1
            if 0 <= idx < len(TARGET_URLS):
                debug_site(TARGET_URLS[idx])
            else:
                print("❌ 無効な番号です")
    except ValueError:
        print("❌ 数字を入力してください")
    except KeyboardInterrupt:
        print("\n👋 デバッグを終了します")

def manual_debug():
    """手動でサイト情報を入力してデバッグ"""
    url = input("デバッグしたいURL: ").strip()
    selector = input("現在のセレクター (空白でスキップ): ").strip()
    
    site_config = {
        "name": "手動入力サイト",
        "url": url,
        "selector": selector if selector else None
    }
    
    debug_site(site_config)

if __name__ == "__main__":
    print("🔧 韓国イベントウォッチャー デバッグツール")
    debug_current_config()
