import sqlite3
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

class EventStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """データベースとテーブルを初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_hash TEXT UNIQUE NOT NULL,
                site_name TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                url TEXT,
                translated_title TEXT,
                translated_content TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notified BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_event_hash(self, site_name: str, title: str, content: str) -> str:
        """イベントの一意性を判定するためのハッシュを生成"""
        combined = f"{site_name}:{title}:{content}"
        return hashlib.md5(combined.encode('utf-8')).hexdigest()
    
    def is_new_event(self, event_hash: str) -> bool:
        """新規イベントかどうかを判定"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM events WHERE event_hash = ?", (event_hash,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count == 0
    
    def save_event(self, event_data: Dict) -> bool:
        """イベント情報をデータベースに保存"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (
                    event_hash, site_name, title, content, url,
                    translated_title, translated_content, summary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_data['event_hash'],
                event_data['site_name'],
                event_data['title'],
                event_data.get('content', ''),
                event_data.get('url', ''),
                event_data.get('translated_title', ''),
                event_data.get('translated_content', ''),
                event_data.get('summary', '')
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            # 重複の場合
            return False
        except Exception as e:
            print(f"Error saving event: {e}")
            return False
    
    def get_recent_events(self, limit: int = 10) -> List[Dict]:
        """最近のイベントを取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'id': row[0],
                'event_hash': row[1],
                'site_name': row[2],
                'title': row[3],
                'content': row[4],
                'url': row[5],
                'translated_title': row[6],
                'translated_content': row[7],
                'summary': row[8],
                'created_at': row[9],
                'notified': row[10]
            })
        
        conn.close()
        return events