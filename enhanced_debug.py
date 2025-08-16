# enhanced_debug.py - より詳細なHTML構造解析
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def analyze_site_deep(url, site_name):
    """サイトのHTML構造を詳細に分析"""
    print(f"\n{'='*80}")
    print(f"🔬 詳細分析: {site_name}")
    print(f"URL: {url}")
    print(f"{'='*80}")
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 1. 全体的なリンク分析
        all_links = soup.find_all("a", href=True)
        print(f"📊 総リンク数: {len(all_links)}")
        
        # 2. イベント関連っぽいリンクを探す
        event_patterns = [
            r'event', r'イベント', r'이벤트',
            r'popup', r'팝업', r'ポップアップ',
            r'news', r'ニュース', r'뉴스',
            r'notice', r'お知らせ', r'공지',
            r'detail', r'詳細', r'상세'
        ]
        
        print(f"\n🎯 イベント関連リンクの分析:")
        event_links = []
        
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # イベント関連キーワードのチェック
            combined_text = (href + ' ' + text).lower()
            if any(re.search(pattern, combined_text, re.IGNORECASE) for pattern in event_patterns):
                event_links.append({
                    'href': href,
                    'text': text[:100],
                    'parent_class': link.parent.get('class') if link.parent else None,
                    'parent_tag': link.parent.name if link.parent else None,
                    'link_class': link.get('class')
                })
        
        print(f"   見つかったイベント関連リンク: {len(event_links)}個")
        
        # 3. 上位10個のイベントリンクを詳細表示
        for i, link_info in enumerate(event_links[:10]):
            print(f"\n--- イベントリンク {i+1} ---")
            print(f"href: {link_info['href']}")
            print(f"text: {link_info['text']}")
            print(f"parent: <{link_info['parent_tag']} class='{link_info['parent_class']}'>")
            print(f"link class: {link_info['link_class']}")
        
        # 4. 推奨セレクターを生成
        print(f"\n💡 推奨セレクター:")
        generate_selectors_from_analysis(event_links, soup)
        
        # 5. 一般的な構造パターンを調査
        print(f"\n🏗️ HTML構造パターン:")
        analyze_common_patterns(soup)
        
    except Exception as e:
        print(f"❌ エラー: {e}")

def generate_selectors_from_analysis(event_links, soup):
    """分析結果から適切なセレクターを提案"""
    if not event_links:
        print("   ❌ イベント関連リンクが見つかりません")
        return
    
    # 親要素のクラス分析
    parent_classes = {}
    link_classes = {}
    href_patterns = {}
    
    for link in event_links:
        # 親のクラス
        if link['parent_class']:
            for cls in link['parent_class']:
                parent_classes[cls] = parent_classes.get(cls, 0) + 1
        
        # リンクのクラス
        if link['link_class']:
            for cls in link['link_class']:
                link_classes[cls] = link_classes.get(cls, 0) + 1
        
        # hrefパターン
        href = link['href']
        for pattern in ['/event', '/detail', '/popup', '/news']:
            if pattern in href.lower():
                href_patterns[pattern] = href_patterns.get(pattern, 0) + 1
    
    print("   クラスベースセレクター:")
    for cls, count in sorted(parent_classes.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"     .{cls} a → {count}個のリンク")
    
    for cls, count in sorted(link_classes.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"     a.{cls} → {count}個のリンク")
    
    print("   hrefベースセレクター:")
    for pattern, count in sorted(href_patterns.items(), key=lambda x: x[1], reverse=True):
        print(f"     a[href*='{pattern}'] → {count}個のリンク")

def analyze_common_patterns(soup):
    """よくある構造パターンを分析"""
    # リスト構造
    lists = soup.find_all(['ul', 'ol'])
    print(f"   リスト要素: {len(lists)}個")
    
    for i, lst in enumerate(lists[:3]):
        items = lst.find_all('li')
        if items:
            print(f"     リスト{i+1}: {len(items)}個のアイテム")
            # 最初のアイテムのリンクをチェック
            first_item = items[0]
            link = first_item.find('a')
            if link:
                print(f"       例: {link.get('href', 'no-href')} - {link.get_text(strip=True)[:50]}")
    
    # カード/アイテム構造
    card_patterns = ['.card', '.item', '.box', '.post', '.article', '.event']
    for pattern in card_patterns:
        elements = soup.select(pattern)
        if elements:
            print(f"   {pattern}: {len(elements)}個")
            # 最初の要素のリンクをチェック
            first = elements[0]
            link = first.find('a')
            if link:
                print(f"     例: {link.get('href', 'no-href')} - {link.get_text(strip=True)[:50]}")

def analyze_specific_sites():
    """問題のあるサイトを集中分析"""
    problem_sites = [
        {
            "name": "MEGABOX イベント", 
            "url": "https://www.megabox.co.kr/event"
        },
        {
            "name": "CGV イベント",
            "url": "https://www.cgv.co.kr/culture-event/event/"
        },
        {
            "name": "LOTTE CINEMA イベント", 
            "url": "https://www.lottecinema.co.kr/LCWS/Event/EventList.aspx"
        }
    ]
    
    for site in problem_sites:
        analyze_site_deep(site["url"], site["name"])
        
        print("\n" + "="*40)
        input("次のサイトに進むには Enter を押してください...")

if __name__ == "__main__":
    print("🔬 韓国イベントウォッチャー - 詳細HTML構造解析ツール")
    print("問題のあるサイトを詳細に分析します...")
    analyze_specific_sites()
