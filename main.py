import time
import logging
from typing import List, Dict

# 各モジュールのインポート（実際の実装では相対インポートを使用）
from config import TARGET_URLS, FILTER_KEYWORDS, OPENAI_API_KEY, SLACK_WEBHOOK_URL, DB_PATH, CHECK_INTERVAL
from utils.logger import setup_logger
from scraper.fetcher import EventFetcher
from processor.filter import EventFilter
from processor.translator import EventTranslator
from db.store import EventStore
from notifier.slack import EventNotifier

class KoreaEventBot:
    def __init__(self):
        self.logger = setup_logger()
        self.fetcher = EventFetcher()
        self.filter = EventFilter(FILTER_KEYWORDS)
        self.translator = EventTranslator(OPENAI_API_KEY) if OPENAI_API_KEY else None
        self.store = EventStore(DB_PATH)
        self.notifier = EventNotifier(SLACK_WEBHOOK_URL)
        
        self.logger.info("Korea Event Bot initialized")
    
    def run_single_check(self):
        """1回分のチェック処理を実行"""
        self.logger.info("Starting event check cycle")
        
        try:
            # 1. 全サイトからイベントを取得
            all_events = self.fetcher.fetch_all_events(TARGET_URLS)
            self.logger.info(f"Fetched {len(all_events)} total events")
            
            # 2. 新規イベントのみをフィルタリング
            new_events = []
            for event in all_events:
                event_hash = self.store.generate_event_hash(
                    event['site_name'], 
                    event['title'], 
                    event['content']
                )
                event['event_hash'] = event_hash
                
                if self.store.is_new_event(event_hash):
                    new_events.append(event)
            
            self.logger.info(f"Found {len(new_events)} new events")
            
            if not new_events:
                self.logger.info("No new events found")
                return
            
            # 3. 注目ワードでフィルタリング
            interesting_events = self.filter.filter_events(new_events)
            
            # 4. 翻訳・要約（ChatGPT APIが利用可能な場合）
            if self.translator:
                for event in interesting_events:
                    event = self.translator.translate_and_summarize(event)
            
            # 5. データベースに保存
            for event in interesting_events:
                self.store.save_event(event)
            
            # 6. 通知
            if interesting_events:
                self.notifier.notify_events(interesting_events)
                self.logger.info(f"Notified {len(interesting_events)} interesting events")
            
        except Exception as e:
            self.logger.error(f"Error during event check: {e}")
    
    def run_continuous(self):
        """継続的な監視を実行"""
        self.logger.info(f"Starting continuous monitoring (interval: {CHECK_INTERVAL} seconds)")
        
        while True:
            try:
                self.run_single_check()
                self.logger.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                self.logger.info("Bot stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                self.logger.info("Continuing after error...")
                time.sleep(60)  # エラー後は1分待機

def main():
    """メイン関数"""
    bot = KoreaEventBot()
    
    # 引数に応じて実行モードを切り替え
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # 1回だけ実行
        bot.run_single_check()
    else:
        # 継続実行
        bot.run_continuous()

if __name__ == "__main__":
    main()
