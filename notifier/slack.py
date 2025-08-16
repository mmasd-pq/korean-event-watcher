import requests
import json
from typing import Dict, List
import logging

class EventNotifier:
    def __init__(self, slack_webhook_url: str = None):
        self.slack_webhook_url = slack_webhook_url
        self.logger = logging.getLogger(__name__)
    
    def notify_events(self, events: List[Dict]):
        """イベント情報を通知"""
        if not events:
            self.logger.info("No events to notify")
            return
        
        for event in events:
            if self.slack_webhook_url:
                self.send_slack_notification(event)
            else:
                self.print_notification(event)
    
    def print_notification(self, event: Dict):
        """ターミナルに通知を出力"""
        print("\n" + "="*80)
        print(f"🔥 新着イベント発見！")
        print(f"サイト: {event.get('site_name', 'Unknown')}")
        print(f"タイトル: {event.get('translated_title', event.get('title', ''))}")
        print(f"内容: {event.get('translated_content', event.get('content', ''))}")
        print(f"要約: {event.get('summary', 'No summary')}")
        print(f"URL: {event.get('url', 'No URL')}")
        print("="*80)
    
    def send_slack_notification(self, event: Dict):
        """Slack通知を送信"""
        try:
            message = {
                "text": "🔥 新着イベント発見！",
                "attachments": [
                    {
                        "color": "good",
                        "fields": [
                            {
                                "title": "サイト",
                                "value": event.get('site_name', 'Unknown'),
                                "short": True
                            },
                            {
                                "title": "タイトル",
                                "value": event.get('translated_title', event.get('title', '')),
                                "short": False
                            },
                            {
                                "title": "要約",
                                "value": event.get('summary', 'No summary'),
                                "short": False
                            },
                            {
                                "title": "URL",
                                "value": event.get('url', 'No URL'),
                                "short": False
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                self.slack_webhook_url,
                data=json.dumps(message),
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info("Slack notification sent successfully")
            else:
                self.logger.error(f"Failed to send Slack notification: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error sending Slack notification: {e}")
