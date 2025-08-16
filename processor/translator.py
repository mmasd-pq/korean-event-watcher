from openai import OpenAI
import logging
from typing import Dict, Optional

class EventTranslator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)
    
    def translate_and_summarize(self, event: Dict) -> Dict:
        """イベント情報を翻訳・要約"""
        try:
            title = event.get('title', '')
            content = event.get('content', '')
            
            # 翻訳プロンプト
            translation_prompt = f"""
以下の韓国語のイベント情報を日本語に翻訳してください。
せどり・転売の観点から重要な情報（限定性、価格、数量、期間など）を重視して翻訳してください。

タイトル: {title}
内容: {content}

以下のフォーマットで回答してください：
タイトル（日本語）: [翻訳されたタイトル]
内容（日本語）: [翻訳された内容]
要約: [せどり観点での重要ポイントを3行以内で要約]
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": translation_prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content
            
            # レスポンスを解析
            translated_data = self.parse_translation_result(result_text)
            
            event.update(translated_data)
            
            self.logger.info(f"Translated event: {event.get('title', '')}")
            return event
            
        except Exception as e:
            self.logger.error(f"Error translating event: {e}")
            # 翻訳失敗時はそのまま返す
            return event
    
    def parse_translation_result(self, result_text: str) -> Dict:
        """ChatGPTの翻訳結果を解析"""
        lines = result_text.strip().split('\n')
        translated_data = {
            'translated_title': '',
            'translated_content': '',
            'summary': ''
        }
        
        for line in lines:
            if 'タイトル（日本語）:' in line:
                translated_data['translated_title'] = line.split(':', 1)[1].strip()
            elif '内容（日本語）:' in line:
                translated_data['translated_content'] = line.split(':', 1)[1].strip()
            elif '要約:' in line:
                translated_data['summary'] = line.split(':', 1)[1].strip()
        
        return translated_data