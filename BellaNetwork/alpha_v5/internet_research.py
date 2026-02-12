"""
ИНТЕРНЕТ-ИССЛЕДОВАНИЯ ДЛЯ БЭЛЛЫ (ограниченный доступ)
"""

import requests
from bs4 import BeautifulSoup
import json
from typing import Optional, List
import re

class InternetResearch:
    """Простой интернет-поиск для Бэллы"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def simple_search(self, query: str, max_results: int = 3) -> List[dict]:
        """Простой поиск через DuckDuckGo HTML"""
        try:
            url = f"https://duckduckgo.com/html/?q={query}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Парсим результаты
            for result in soup.find_all('a', class_='result__url', limit=max_results):
                title = result.get_text(strip=True)
                link = result.get('href')
                
                if title and link and 'http' in link:
                    # Получаем краткое описание
                    desc_elem = result.find_next('a', class_='result__snippet')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    results.append({
                        'title': title,
                        'url': link,
                        'description': description[:200]
                    })
            
            return results
            
        except Exception as e:
            print(f">> Интернет поиск ошибка: {e}")
            return []
    
    def get_wikipedia_summary(self, topic: str) -> Optional[str]:
        """Получает краткое описание из Wikipedia"""
        try:
            url = f"https://ru.wikipedia.org/api/rest_v1/page/summary/{topic}"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('extract', '')[:500]
        
        except:
            pass
        
        return None
    
    def research_topic(self, topic: str) -> dict:
        """Исследует тему в интернете"""
        print(f">> 🔍 Исследую тему: {topic}")
        
        research = {
            'topic': topic,
            'wikipedia_summary': None,
            'search_results': [],
            'key_points': []
        }
        
        # 1. Wikipedia
        research['wikipedia_summary'] = self.get_wikipedia_summary(topic)
        
        # 2. Поиск
        research['search_results'] = self.simple_search(topic, max_results=5)
        
        # 3. Извлекаем ключевые моменты
        all_text = ""
        if research['wikipedia_summary']:
            all_text += research['wikipedia_summary'] + " "
        
        for result in research['search_results']:
            all_text += result.get('description', '') + " "
        
        # Простая экстракция ключевых слов
        words = re.findall(r'\b[а-яА-Яa-zA-Z]{4,}\b', all_text.lower())
        from collections import Counter
        common_words = Counter(words).most_common(10)
        
        research['key_points'] = [word for word, count in common_words 
                                 if word not in ['это', 'что', 'как', 'для', 'очень']]
        
        return research

# Интеграция в consciousness_core_v5_3.py
def add_internet_to_consciousness():
    """Добавляет интернет-модуль в сознание"""
    # В __init__ DynamicConsciousness:
    print(">> 🌐 Инициализация Internet Research...")
    try:
        from internet_research import InternetResearch
        self.internet_research = InternetResearch()
        print(">> ✅ Internet Research загружен")
    except Exception as e:
        print(f">> ⚠️ Internet Research не загрузился: {e}")
        self.internet_research = None