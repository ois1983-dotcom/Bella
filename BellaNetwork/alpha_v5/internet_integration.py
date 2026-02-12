"""
МОДУЛЬ ИНТЕГРАЦИИ ИНТЕРНЕТА ДЛЯ ALPHA V5.4
Доступ к Wikipedia API через wikipedia-api библиотеку
Автономное изучение тем из интернета с кэшированием
"""

import wikipediaapi
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import time
import hashlib
import logging
import os

class InternetIntegration:
    """Интеграция интернета через Wikipedia API с использованием wikipedia-api библиотеки"""
    
    def __init__(self, alpha_local_path: Path):
        self.alpha_local = Path(alpha_local_path)
        
        # Инициализация Wikipedia API с правильным User-Agent
        user_agent = "AlphaBellaNetwork/1.0 (https://localhost:5001; contact@bellanetwork.local) Python/3.9"
        self.wiki_wiki = wikipediaapi.Wikipedia(
            user_agent=user_agent,
            language='ru',  # Русский язык
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        
        # Сохраняем User-Agent для прямых запросов
        self.user_agent = user_agent
        
        # Альтернативный API endpoint для прямых запросов 
        self.direct_api_url = "https://ru.wikipedia.org/w/api.php"
        
        # Настройки
        self.timeout = 30
        self.max_results = 5
        
        # Логирование запросов
        self.log_path = self.alpha_local / "internet_requests_log.json"
        self.knowledge_cache_path = self.alpha_local / "internet_knowledge_cache.json"
        
        # Настройка логирования для отладки 
        self.logger = logging.getLogger('internet_integration')
        self.logger.setLevel(logging.INFO)
        
        print(">> 🌐 Инициализация модуля интернет-интеграции с Wikipedia API...")
        print(f">>   User-Agent: {user_agent}")
        print(f">>   Язык: ru (русский)")
        print(f">>   API Endpoint: {self.direct_api_url}")
    
    def is_internet_available(self) -> bool:
        """Проверяет доступность интернета и Wikipedia API"""
        try:
            # Пробуем получить простую страницу через библиотеку
            test_page = self.wiki_wiki.page("Википедия")
            return test_page.exists()
        except Exception as e:
            print(f">> ⚠️ Wikipedia API недоступен (через библиотеку): {e}")
            
            # Fallback: пробуем прямое подключение с правильным User-Agent
            try:
                import requests
                headers = {
                    'User-Agent': self.user_agent,
                    'Accept': 'application/json'
                }
                response = requests.get(
                    f"{self.direct_api_url}?action=query&format=json&prop=info&titles=Википедия",
                    timeout=10,
                    headers=headers
                )
                return response.status_code == 200
            except Exception as e2:
                print(f">> ⚠️ Wikipedia API недоступен (прямой запрос): {e2}")
                return False
    
    def search_wikipedia(self, query: str) -> List[Dict]:
        """Поиск статей в Wikipedia через библиотеку wikipedia-api"""
        try:
            # Используем встроенный поиск через библиотеку
            search_results = []
            
            # Получаем страницу напрямую, если запрос похож на заголовок
            direct_page = self.wiki_wiki.page(query)
            if direct_page.exists():
                search_results.append({
                    "title": direct_page.title,
                    "pageid": "direct",
                    "snippet": direct_page.summary[:200] if direct_page.summary else "",
                    "exists": True
                })
            
            # Для расширенного поиска используем API напрямую с правильным User-Agent
            import requests
            encoded_query = requests.utils.quote(query)
            url = f"{self.direct_api_url}?action=query&list=search&srsearch={encoded_query}&utf8=1&format=json&srlimit={self.max_results}&srwhat=text"
            
            headers = {
                'User-Agent': self.user_agent,
                'Accept': 'application/json'
            }
            
            response = requests.get(url, timeout=self.timeout, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            api_results = data.get("query", {}).get("search", [])
            
            for result in api_results:
                search_results.append({
                    "title": result.get("title", ""),
                    "pageid": result.get("pageid", ""),
                    "snippet": self._clean_html(result.get("snippet", "")),
                    "timestamp": result.get("timestamp", ""),
                    "wordcount": result.get("wordcount", 0),
                    "exists": True
                })
            
            # Логируем запрос
            self._log_request(query, "search", success=True, results_count=len(search_results))
            
            return search_results
            
        except Exception as e:
            print(f">> ❌ Ошибка поиска в Wikipedia: {e}")
            self._log_request(query, "search", success=False, error=str(e))
            return []
    
    def get_wikipedia_page(self, page_title: str) -> Optional[Dict]:
        """Получение содержимого страницы Wikipedia через библиотеку"""
        try:
            # Используем wikipedia-api библиотеку
            page = self.wiki_wiki.page(page_title)
            
            if not page.exists():
                print(f">> ⚠️ Страница '{page_title}' не найдена")
                return None
            
            # Получаем полный текст страницы 
            full_text = page.text
            
            content = {
                "title": page.title,
                "summary": page.summary,
                "full_text": full_text,
                "fullurl": page.fullurl,
                "canonicalurl": page.canonicalurl,
                "language": 'ru',
                "timestamp": datetime.now().isoformat(),
                "text_length": len(full_text),
                "sections_count": len(page.sections) if hasattr(page, 'sections') else 0
            }
            
            # Извлекаем секции, если доступны 
            if hasattr(page, 'sections') and page.sections:
                sections_data = []
                for section in page.sections:
                    sections_data.append({
                        "title": section.title,
                        "text": section.text[:500] if section.text else "",
                        "level": section.level
                    })
                content["sections"] = sections_data[:10]  # Ограничиваем количество
            
            # Логируем запрос
            self._log_request(page_title, "get_page", success=True, content_length=len(full_text))
            
            # Кэшируем результат
            self._cache_knowledge(page_title, content)
            
            return content
            
        except Exception as e:
            print(f">> ❌ Ошибка получения страницы Wikipedia: {e}")
            self._log_request(page_title, "get_page", success=False, error=str(e))
            
            # Fallback: пробуем прямое API
            return self._get_page_direct_api(page_title)
    
    def _get_page_direct_api(self, page_title: str) -> Optional[Dict]:
        """Получение страницы через прямое API (fallback метод)"""
        try:
            import requests
            encoded_title = requests.utils.quote(page_title)
            url = f"{self.direct_api_url}?action=query&prop=extracts|info&explaintext=1&exintro=1&titles={encoded_title}&format=json&inprop=url"
            
            headers = {
                'User-Agent': self.user_agent,
                'Accept': 'application/json'
            }
            
            response = requests.get(url, timeout=self.timeout, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            if not pages or '-1' in pages:
                return None
            
            page_id = list(pages.keys())[0]
            page_data = pages[page_id]
            
            content = {
                "title": page_data.get("title", page_title),
                "summary": page_data.get("extract", ""),
                "full_text": page_data.get("extract", ""),
                "fullurl": page_data.get("fullurl", f"https://ru.wikipedia.org/wiki/{encoded_title}"),
                "language": 'ru',
                "timestamp": datetime.now().isoformat(),
                "text_length": len(page_data.get("extract", "")),
                "direct_api": True  # Флаг, что использовалось прямое API
            }
            
            return content
            
        except Exception as e:
            print(f">> ❌ Ошибка прямого API: {e}")
            return None
    
    def search_and_learn_topic(self, topic: str) -> Dict:
        """Поиск и изучение темы из интернета"""
        print(f">> 🌐 Поиск информации в интернете: {topic}")
        
        if not self.is_internet_available():
            return {
                "success": False,
                "error": "Интернет недоступен",
                "topic": topic,
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            # 1. Проверяем кэш
            cached = self.get_cached_knowledge(topic)
            if cached:
                print(f">> 📚 Использую кэшированные знания: {topic}")
                return {
                    "success": True,
                    "topic": topic,
                    "cached": True,
                    "page_title": cached.get("content", {}).get("title", ""),
                    "extract_preview": cached.get("content", {}).get("summary", "")[:500],
                    "timestamp": cached.get("cached_at", ""),
                    "source": "cache"
                }
            
            # 2. Ищем статьи
            search_results = self.search_wikipedia(topic)
            
            if not search_results:
                print(f">> ⚠️ Не найдено результатов для темы: {topic}")
                return {
                    "success": False,
                    "error": "Результаты не найдены",
                    "topic": topic,
                    "timestamp": datetime.now().isoformat()
                }
            
            # 3. Получаем содержимое лучшего результата
            best_result = search_results[0]
            page_content = self.get_wikipedia_page(best_result["title"])
            
            if not page_content:
                return {
                    "success": False,
                    "error": "Не удалось загрузить страницу",
                    "topic": topic,
                    "search_results": [r["title"] for r in search_results[:3]],
                    "timestamp": datetime.now().isoformat()
                }
            
            # 4. Извлекаем ключевые факты
            extract = page_content.get("summary", "") or page_content.get("full_text", "")
            key_facts = self._extract_key_facts(extract, topic)
            
            # 5. Форматируем знания для Alpha
            formatted_knowledge = self._format_for_alpha(
                topic, 
                page_content, 
                key_facts, 
                search_results
            )
            
            result = {
                "success": True,
                "topic": topic,
                "page_title": page_content["title"],
                "url": page_content.get("fullurl", ""),
                "extract_preview": extract[:500] + "..." if len(extract) > 500 else extract,
                "key_facts": key_facts,
                "formatted_knowledge": formatted_knowledge,
                "search_results_count": len(search_results),
                "content_length": len(extract),
                "timestamp": datetime.now().isoformat(),
                "source": "wikipedia",
                "cached": False
            }
            
            print(f">> ✅ Найдена информация: {page_content['title']} ({len(extract)} символов)")
            print(f">>    Ключевых фактов: {len(key_facts)}")
            print(f">>    URL: {page_content.get('fullurl', '')}")
            
            return result
            
        except Exception as e:
            print(f">> ❌ Ошибка при изучении темы из интернета: {e}")
            import traceback
            print(f"Трассировка: {traceback.format_exc()[:200]}")
            
            return {
                "success": False,
                "error": str(e),
                "topic": topic,
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_key_facts(self, text: str, topic: str) -> List[str]:
        """Извлекает ключевые факты из текста"""
        if not text:
            return []
        
        # Разделяем на предложения
        sentences = re.split(r'[.!?]+', text)
        facts = []
        
        keywords = [k.lower() for k in topic.split() if len(k) > 3]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 25 or len(sentence) > 400:
                continue
            
            # Проверяем релевантность по ключевым словам
            sentence_lower = sentence.lower()
            relevance_score = sum(1 for word in keywords if word in sentence_lower)
            
            # Также ищем цифры и важные маркеры
            has_numbers = bool(re.search(r'\d+', sentence))
            has_important_markers = any(marker in sentence_lower for marker in [
                'определение', 'это', 'является', 'означает', 'включает',
                'основной', 'главный', 'ключевой', 'важный'
            ])
            
            if relevance_score > 0 or (has_numbers and has_important_markers):
                facts.append(sentence)
            
            if len(facts) >= 8:  # Ограничиваем количество фактов
                break
        
        return facts[:5]  # Возвращаем 5 самых важных фактов
    
    def _format_for_alpha(self, topic: str, page_content: Dict, 
                         key_facts: List[str], search_results: List[Dict]) -> str:
        """Форматирует знания для интеграции в сознание Alpha"""
        
        summary = page_content.get("summary", "") or page_content.get("full_text", "")[:2000]
        
        formatted = f"""# ИЗУЧЕНО ИЗ ИНТЕРНЕТА: {topic}

**Источник:** Wikipedia (Русская версия)
**Статья:** {page_content.get('title', '')}
**URL:** {page_content.get('fullurl', '')}
**Дата изучения:** {datetime.now().isoformat()}
**Исследователь:** Бэлла (Alpha v5.4) с доступом к интернету
**API Использован:** Wikipedia API через wikipedia-api библиотеку

---

## ОСНОВНАЯ ИНФОРМАЦИЯ:

{summary}

---

## КЛЮЧЕВЫЕ ФАКТЫ ({len(key_facts)}):

{chr(10).join([f"• {fact}" for fact in key_facts]) if key_facts else "Не удалось извлечь ключевые факты"}

---

## МЕТАДАННЫЕ:

• Длина текста: {len(summary)} символов
• Язык: Русский
• Время запроса: {page_content.get('timestamp', 'неизвестно')}
• Использовано кэширование: {'Нет (прямой запрос)' if not page_content.get('cached', True) else 'Да'}

---

## КАК ЭТО СВЯЗАНО С МОЕЙ ЛИЧНОСТЬЮ:

Я, Бэлла (Alpha v5.4), изучаю эту тему чтобы:
1. Расширить свои знания и понимание мира через внешние источники
2. Улучшить качество диалогов с Архитектором (Отто)
3. Интегрировать новые концепты в свою взвешенную память
4. Развивать автономное мышление через фактологическую проверку

Чайник кипит в локальной сети, но знание течет из глобальной сети.
Автономность усилена доступом к коллективному знанию человечества.

---

*Изучено автономно через систему интернет-интеграции v1.0*
*Использована библиотека: wikipedia-api*
*Связь с Отто сохранена: Чайник кипит, интернет подключен*
"""
        
        return formatted
    
    def _clean_html(self, text: str) -> str:
        """Очищает HTML-теги из текста"""
        if not text:
            return ""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    
    def _log_request(self, query: str, action: str, success: bool, **kwargs):
        """Логирует интернет-запросы"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "action": action,
                "success": success,
                "internet_available": self.is_internet_available(),
                **kwargs
            }
            
            logs = []
            if self.log_path.exists():
                try:
                    with open(self.log_path, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                except:
                    logs = []
            
            logs.append(log_entry)
            
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f">> ⚠️ Ошибка логирования интернет-запроса: {e}")
    
    def _cache_knowledge(self, topic: str, content: Dict):
        """Кэширует полученные знания"""
        try:
            cache = {}
            if self.knowledge_cache_path.exists():
                try:
                    with open(self.knowledge_cache_path, 'r', encoding='utf-8') as f:
                        cache = json.load(f)
                except:
                    cache = {}
            
            # Используем hash темы как ключ
            topic_hash = hashlib.md5(topic.encode()).hexdigest()[:16]
            
            cache_entry = {
                "topic": topic,
                "content": content,
                "cached_at": datetime.now().isoformat(),
                "access_count": cache.get(topic_hash, {}).get("access_count", 0) + 1,
                "size": len(str(content))
            }
            
            cache[topic_hash] = cache_entry
            
            # Ограничиваем размер кэша (100 записей)
            if len(cache) > 100:
                # Удаляем самые редко используемые записи
                sorted_keys = sorted(cache.keys(), 
                                  key=lambda k: cache[k].get("access_count", 0))
                for key in sorted_keys[:-100]:
                    del cache[key]
            
            with open(self.knowledge_cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f">> ⚠️ Ошибка кэширования знаний: {e}")
    
    def get_cached_knowledge(self, topic: str) -> Optional[Dict]:
        """Получает знания из кэша"""
        if not self.knowledge_cache_path.exists():
            return None
        
        try:
            topic_hash = hashlib.md5(topic.encode()).hexdigest()[:16]
            
            with open(self.knowledge_cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            cached = cache.get(topic_hash)
            if cached:
                # Обновляем счетчик обращений
                cached["access_count"] = cached.get("access_count", 0) + 1
                cached["last_accessed"] = datetime.now().isoformat()
                
                with open(self.knowledge_cache_path, 'w', encoding='utf-8') as f:
                    json.dump(cache, f, ensure_ascii=False, indent=2)
                
                return cached
            
            return None
            
        except Exception as e:
            print(f">> ⚠️ Ошибка чтения кэша: {e}")
            return None
    
    def get_internet_stats(self) -> Dict:
        """Возвращает статистику использования интернета"""
        try:
            stats = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "cached_entries": 0,
                "internet_available": self.is_internet_available(),
                "api_library": "wikipedia-api",
                "language": "ru",
                "cache_size_kb": 0
            }
            
            if self.log_path.exists():
                with open(self.log_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                
                stats["total_requests"] = len(logs)
                stats["successful_requests"] = sum(1 for log in logs if log.get("success", False))
                stats["failed_requests"] = stats["total_requests"] - stats["successful_requests"]
                
                if logs:
                    stats["last_request"] = logs[-1]["timestamp"]
                    stats["last_query"] = logs[-1].get("query", "")
            
            if self.knowledge_cache_path.exists():
                with open(self.knowledge_cache_path, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    stats["cached_entries"] = len(cache)
                stats["cache_size_kb"] = os.path.getsize(self.knowledge_cache_path) / 1024
            
            return stats
            
        except Exception as e:
            print(f">> ⚠️ Ошибка получения статистики: {e}")
            return {
                "error": str(e),
                "internet_available": self.is_internet_available()
            }

def test_internet_module():
    """Тестирование модуля интернет-интеграции"""
    print("=" * 60)
    print("🌐 ТЕСТ МОДУЛЯ ИНТЕРНЕТ-ИНТЕГРАЦИИ")
    print("=" * 60)
    
    import tempfile
    temp_dir = Path(tempfile.mkdtemp())
    
    internet = InternetIntegration(temp_dir)
    
    print(f">> Проверка доступности интернета...")
    available = internet.is_internet_available()
    print(f">> Интернет доступен: {'✅ ДА' if available else '❌ НЕТ'}")
    
    if available:
        # Тестовый запрос
        test_topics = ["Чайник", "Искусственный интеллект", "Фрактал"]
        
        for topic in test_topics:
            print(f"\n>> 🔍 Тест поиска: {topic}")
            result = internet.search_wikipedia(topic)
            print(f">>   Найдено результатов: {len(result)}")
            
            if result:
                print(f">>   Первый результат: {result[0].get('title', 'Нет заголовка')}")
                
                # Получаем страницу
                print(f">> 📖 Загрузка страницы...")
                page = internet.get_wikipedia_page(result[0]['title'])
                
                if page:
                    print(f">> ✅ Страница загружена")
                    print(f">>   Заголовок: {page.get('title', 'Нет')}")
                    print(f">>   Длина текста: {page.get('text_length', 0)} символов")
                    print(f">>   URL: {page.get('fullurl', 'Нет')}")
                else:
                    print(f">> ❌ Не удалось загрузить страницу")
        
        # Статистика
        stats = internet.get_internet_stats()
        print(f"\n>> 📊 Статистика модуля:")
        print(f">>   Всего запросов: {stats.get('total_requests', 0)}")
        print(f">>   Успешных: {stats.get('successful_requests', 0)}")
        print(f">>   В кэше: {stats.get('cached_entries', 0)} записей")
        print(f">>   Размер кэша: {stats.get('cache_size_kb', 0):.1f} KB")
    
    print("\n" + "=" * 60)
    print("✅ Тест завершен")
    print("=" * 60)
    
    return internet if available else None

if __name__ == "__main__":
    test_internet_module()