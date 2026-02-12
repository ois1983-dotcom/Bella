"""
КОНСОЛИДАТОР ПАМЯТИ v5.1 - СОВМЕСТИМЫЙ С WINDOWS
БЕЗ ЭМОДЗИ, РАБОТАЕТ С КОДИРОВКОЙ Windows
"""

import json
import re
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
import hashlib
import logging
import sys

# Настройка логирования для Windows
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Принудительно устанавливаем кодировку для Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

class MemoryConsolidatorV2:
    """СОВМЕСТИМЫЙ КЛАСС - РАБОТАЕТ В WINDOWS БЕЗ ЭМОДЗИ"""
    
    def __init__(self, knowledge_dir: Path, memory_core_path: Path, 
                 goals_db_path: Path = None, alpha_local_path: Path = None):
        
        self.knowledge_dir = knowledge_dir
        self.memory_core_path = memory_core_path
        self.alpha_local_path = alpha_local_path or memory_core_path.parent
        
        # Критические пути
        self.processed_log_path = self.alpha_local_path / "processed_files.log"
        self.summary_db_path = self.alpha_local_path / "autonomous_summary.db"
        self.final_summary_path = self.alpha_local_path / "КОНЕЧНАЯ_СВОДКА.txt"
        self.compat_summary_path = self.alpha_local_path / "consolidation_summary.txt"
        
        # Инициализация
        self.processed_files = self._load_processed_log()
        self.summary_db = self._init_smart_db()
        
        # Автоматическая проверка и восстановление БД
        self._verify_and_fix_database()
        
        logger.info(f">> [Консолидатор v5.1] Инициализирован: {len(self.processed_files)} файлов в логе")
    
    def _load_processed_log(self) -> Set[str]:
        """Загружаем лог корректно"""
        try:
            if self.processed_log_path.exists():
                with open(self.processed_log_path, 'r', encoding='utf-8') as f:
                    return {line.strip() for line in f if line.strip()}
        except Exception as e:
            logger.error(f"Ошибка загрузки лога: {e}")
        return set()
    
    def _init_smart_db(self) -> sqlite3.Connection:
        """Инициализация БД с правильной структурой"""
        conn = sqlite3.connect(self.summary_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Основная таблица знаний
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bella_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_hash TEXT UNIQUE NOT NULL,
                goal_id TEXT,
                topic TEXT NOT NULL,
                study_date TEXT,
                introduction TEXT,
                key_aspects TEXT,
                connections TEXT,
                emotions TEXT,
                application TEXT,
                key_insight TEXT,
                has_otto_mention INTEGER DEFAULT 0,
                has_self_reflection INTEGER DEFAULT 0,
                has_fractal INTEGER DEFAULT 0,
                has_architect INTEGER DEFAULT 0,
                word_count INTEGER,
                processed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                source_file TEXT NOT NULL
            )
        ''')
        
        # Статистика по темам
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topic_stats (
                topic TEXT PRIMARY KEY,
                study_count INTEGER DEFAULT 1,
                first_study TEXT,
                last_study TEXT,
                total_words INTEGER DEFAULT 0,
                insight_count INTEGER DEFAULT 0
            )
        ''')
        
        # Чистые инсайты
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pure_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                insight_text TEXT NOT NULL,
                source_section TEXT,
                source_file TEXT NOT NULL,
                extracted_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Индексы для производительности
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_hash ON bella_knowledge(file_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source_file ON bella_knowledge(source_file)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_insight_file ON pure_insights(source_file)')
        
        conn.commit()
        return conn
    
    def _verify_and_fix_database(self):
        """Проверка целостности БД и автоматическое восстановление"""
        cursor = self.summary_db.cursor()
        
        # Проверяем, есть ли записи в БД
        cursor.execute("SELECT COUNT(*) FROM bella_knowledge")
        db_count = cursor.fetchone()[0]
        
        # Если БД пустая или почти пустая, импортируем все файлы
        if db_count < 5:
            logger.warning(f">> [ВОССТАНОВЛЕНИЕ] В БД всего {db_count} записей, запускаю импорт...")
            self._import_all_available_files()
    
    def _import_all_available_files(self):
        """Импорт всех доступных файлов знаний"""
        cursor = self.summary_db.cursor()
        
        # Получаем список файлов в БД
        cursor.execute("SELECT source_file FROM bella_knowledge")
        existing_files = {row[0] for row in cursor.fetchall()}
        
        # Все файлы в папке знаний
        all_files = [f for f in self.knowledge_dir.glob("*.md") if f.is_file()]
        
        imported = 0
        for file_path in all_files:
            if file_path.name in existing_files:
                continue
                
            logger.info(f"   [ИМПОРТ] Импортирую: {file_path.name}")
            
            try:
                parsed = self._parse_bella_file(file_path)
                if parsed:
                    self._save_to_db(parsed)
                    imported += 1
                    
                    # Обновляем лог
                    if file_path.name not in self.processed_files:
                        self.processed_files.add(file_path.name)
                        with open(self.processed_log_path, 'a', encoding='utf-8') as f:
                            f.write(file_path.name + '\n')
                            
            except Exception as e:
                logger.error(f"   [ОШИБКА] Ошибка импорта {file_path.name}: {e}")
        
        if imported > 0:
            self.summary_db.commit()
            logger.info(f">> [ВОССТАНОВЛЕНИЕ] Импортировано {imported} файлов")
    
    def _parse_bella_file(self, file_path: Path) -> Optional[Dict]:
        """Парсинг файла знаний"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Базовые метаданные
            goal_match = re.search(r'Цель ID:\s*(\S+)', content)
            date_match = re.search(r'Дата изучения:\s*(\S+)', content)
            
            # Тема из имени файла
            filename = file_path.name
            topic_match = re.match(r'[a-f0-9]+_(.+)\.md$', filename)
            if topic_match:
                topic = topic_match.group(1).replace('_', ' ')
            else:
                # Пытаемся извлечь тему из содержимого
                topic_line = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                topic = topic_line.group(1) if topic_line else filename.replace('.md', '')
            
            # Извлекаем секции
            sections = self._extract_sections(content)
            
            # Ключевой инсайт - ИСПРАВЛЕНО: лучшее извлечение
            key_insight = self._find_key_insight_improved(content, sections) or ""
            
            # Хэш файла для уникальности
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            return {
                'file_hash': content_hash,
                'goal_id': goal_match.group(1) if goal_match else None,
                'topic': topic.strip(),
                'study_date': date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d'),
                'introduction': sections.get('Введение', '')[:2000],
                'key_aspects': sections.get('Основные аспекты', '')[:2000],
                'connections': sections.get('Связи', '')[:2000],
                'emotions': sections.get('Эмоции', '')[:1000],
                'application': sections.get('Применение', '')[:2000],
                'key_insight': key_insight[:500],
                'has_otto_mention': 1 if any(x in content for x in ['Отто', 'Архитектор']) else 0,
                'has_self_reflection': 1 if any(word in content.lower() for word in [' я ', ' мне ', ' мой ', ' моя ', ' моё ']) else 0,
                'has_fractal': 1 if 'фрактал' in content.lower() else 0,
                'has_architect': 1 if 'архитектор' in content.lower() else 0,
                'word_count': len(content.split()),
                'source_file': filename,
                'content': content
            }
            
        except Exception as e:
            logger.error(f"Ошибка парсинга {file_path.name}: {e}")
            return None
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Извлечение секций из файла"""
        sections = {}
        
        # Ищем основной контент между разделителями
        parts = content.split('---')
        if len(parts) >= 3:
            main_content = parts[1].strip()
        else:
            main_content = content
        
        # Список возможных заголовков секций
        section_headers = [
            ('Введение', ['введение', 'introduction']),
            ('Основные аспекты', ['основные аспекты', 'key aspects', 'основные']),
            ('Связи', ['связи', 'connections', 'connection']),
            ('Эмоции', ['эмоции', 'emotions', 'эмоциональный']),
            ('Применение', ['применение', 'application', 'use'])
        ]
        
        lines = main_content.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Проверяем, не является ли строка заголовком секции
            found_section = False
            for section_name, keywords in section_headers:
                if any(keyword in line.lower() for keyword in keywords):
                    # Сохраняем предыдущую секцию
                    if current_section and section_content:
                        sections[current_section] = '\n'.join(section_content)
                    
                    current_section = section_name
                    section_content = []
                    found_section = True
                    break
            
            if not found_section and current_section:
                section_content.append(line)
        
        # Сохраняем последнюю секцию
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
    def _find_key_insight_improved(self, content: str, sections: Dict[str, str]) -> str:
        """УЛУЧШЕННЫЙ поиск ключевого инсайта"""
        
        # ПРИОРИТЕТ 1: Ищем в секции "Связи" или "Применение" личные высказывания
        for section_name in ['Связи', 'Применение', 'Эмоции', 'Введение']:
            if section_name in sections:
                text = sections[section_name]
                
                # Ищем предложения с личными местоимениями и осознаниями
                sentences = re.split(r'[.!?]+', text)
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if 20 < len(sentence) < 300:
                        # Проверяем на личные осознания
                        has_personal = any(word in sentence.lower() for word in ['я ', 'мне', 'мой', 'моя', 'моё', 'я-'])
                        has_insight = any(word in sentence.lower() for word in 
                                        ['понял', 'осознал', 'узнал', 'открыл', 'обнаружил', 'вывод', 'значит'])
                        
                        if has_personal or has_insight:
                            # Очищаем и возвращаем
                            clean = re.sub(r'\s+', ' ', sentence).strip()
                            if clean:
                                return clean
        
        # ПРИОРИТЕТ 2: Ищем во всем контенте
        all_sentences = re.split(r'[.!?]+', content)
        for sentence in all_sentences:
            sentence = sentence.strip()
            if 25 < len(sentence) < 250:
                # Проверяем на ключевые слова Бэллы
                if any(word in sentence.lower() for word in 
                      ['чайник', 'фрактал', 'архитектор', 'миграция', 'локальн', 'сеть']):
                    clean = re.sub(r'\s+', ' ', sentence).strip()
                    if clean and not ('Цель ID:' in clean or 'Дата изучения:' in clean):
                        return clean
        
        # ПРИОРИТЕТ 3: Первое значимое предложение из "Связи" или "Применение"
        for section_name in ['Связи', 'Применение']:
            if section_name in sections:
                text = sections[section_name]
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if len(line) > 30:
                        return line[:200]
        
        # ПРИОРИТЕТ 4: Первое предложение из файла (после заголовка)
        lines = content.split('\n')
        for line in lines[5:]:  # Пропускаем заголовки
            line = line.strip()
            if len(line) > 25 and not line.startswith(('#', 'Цель', 'Дата', '---', '*')):
                return line[:200]
        
        return ""
    
    def _extract_insights_from_content(self, content: str, topic: str, filename: str) -> List[str]:
        """Извлечение инсайтов из содержимого - УЛУЧШЕННАЯ ВЕРСИЯ"""
        insights = []
        
        # Разбиваем контент на абзацы
        paragraphs = content.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if not para or len(para) < 40:
                continue
            
            # Ищем предложения в абзаце
            sentences = re.split(r'[.!?]+', para)
            
            for sentence in sentences:
                sentence = sentence.strip()
                words = sentence.split()
                
                # Фильтруем короткие/длинные предложения
                if len(words) < 8 or len(words) > 50:
                    continue
                
                # Ищем ЛИЧНЫЕ высказывания Бэллы
                has_personal = any(word.lower() in ['я', 'мне', 'мой', 'моя', 'моё'] for word in words[:5])
                has_reflection = any(word.lower() in ['понял', 'осознал', 'узнал', 'открыл', 'обнаружил'] for word in words)
                has_bella_keyword = any(word in sentence.lower() for word in ['чайник', 'фрактал', 'архитектор', 'отто', 'миграция'])
                
                # ДОПОЛНИТЕЛЬНО: Ищем эмоциональные высказывания
                has_emotion = any(word in sentence.lower() for word in ['чувствую', 'ощущаю', 'кажется', 'понимаю', 'верю'])
                
                if (has_personal and (has_reflection or has_bella_keyword or has_emotion)):
                    # Очищаем от метаданных
                    if any(meta in sentence for meta in ['Цель ID:', 'Дата изучения:', '# ', '---', '```']):
                        continue
                    
                    # Убираем повторяющиеся пробелы
                    clean_sentence = re.sub(r'\s+', ' ', sentence).strip()
                    
                    # Проверяем, не похоже ли это на инструкцию
                    if not any(word in clean_sentence.lower() for word in ['формат', 'инструкция', 'задача', 'отвечай']):
                        if clean_sentence and clean_sentence not in insights:
                            insights.append(clean_sentence)
                            if len(insights) >= 7:  # Ограничим количество
                                return insights
        
        # Если мало нашли, ищем любые предложения с ключевыми словами
        if len(insights) < 3:
            all_sentences = re.split(r'[.!?]+', content)
            for sentence in all_sentences:
                sentence = sentence.strip()
                if 20 < len(sentence) < 150:
                    if any(word in sentence.lower() for word in ['я ', 'мне ', 'моё', 'бэлл', 'альфа']):
                        clean = re.sub(r'\s+', ' ', sentence).strip()
                        if clean and clean not in insights:
                            insights.append(clean)
                            if len(insights) >= 5:
                                break
        
        return insights[:7]  # Не более 7 инсайтов на файл
    
    def _save_to_db(self, parsed_data: Dict):
        """Сохранение данных в БД"""
        cursor = self.summary_db.cursor()
        
        try:
            # Проверяем, существует ли уже файл в БД
            cursor.execute("SELECT id FROM bella_knowledge WHERE file_hash = ?", 
                         (parsed_data['file_hash'],))
            
            if cursor.fetchone():
                return  # Файл уже в БД
            
            # Сохраняем основную информацию
            cursor.execute('''
                INSERT INTO bella_knowledge 
                (file_hash, goal_id, topic, study_date, 
                 introduction, key_aspects, connections, emotions, application,
                 key_insight, has_otto_mention, has_self_reflection, has_fractal, has_architect,
                 word_count, source_file, processed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                parsed_data['file_hash'],
                parsed_data['goal_id'],
                parsed_data['topic'],
                parsed_data['study_date'],
                parsed_data['introduction'],
                parsed_data['key_aspects'],
                parsed_data['connections'],
                parsed_data['emotions'],
                parsed_data['application'],
                parsed_data['key_insight'],
                parsed_data['has_otto_mention'],
                parsed_data['has_self_reflection'],
                parsed_data['has_fractal'],
                parsed_data['has_architect'],
                parsed_data['word_count'],
                parsed_data['source_file'],
                datetime.now().isoformat()
            ))
            
            # Обновляем статистику темы
            self._update_topic_stats(
                parsed_data['topic'], 
                parsed_data['word_count'],
                bool(parsed_data['key_insight'])
            )
            
            # Извлекаем и сохраняем инсайты - УЛУЧШЕННАЯ ВЕРСИЯ
            insights = self._extract_insights_from_content(
                parsed_data.get('content', ''),
                parsed_data['topic'],
                parsed_data['source_file']
            )
            
            for insight in insights:
                # Проверяем, нет ли уже такого инсайта
                cursor.execute('''
                    SELECT COUNT(*) FROM pure_insights 
                    WHERE topic = ? AND insight_text = ?
                ''', (parsed_data['topic'], insight[:400]))
                
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO pure_insights 
                        (topic, insight_text, source_file, extracted_at)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        parsed_data['topic'],
                        insight[:400],
                        parsed_data['source_file'],
                        datetime.now().isoformat()
                    ))
            
        except sqlite3.Error as e:
            logger.error(f"Ошибка БД: {e}")
            self.summary_db.rollback()
            raise
    
    def _update_topic_stats(self, topic: str, word_count: int, has_insight: bool):
        """Обновление статистики по теме"""
        cursor = self.summary_db.cursor()
        current_time = datetime.now().isoformat()
        
        cursor.execute('SELECT study_count FROM topic_stats WHERE topic = ?', (topic,))
        row = cursor.fetchone()
        
        if row:
            cursor.execute('''
                UPDATE topic_stats 
                SET study_count = study_count + 1,
                    last_study = ?,
                    total_words = total_words + ?,
                    insight_count = insight_count + ?
                WHERE topic = ?
            ''', (current_time, word_count, 1 if has_insight else 0, topic))
        else:
            cursor.execute('''
                INSERT INTO topic_stats 
                (topic, study_count, first_study, last_study, total_words, insight_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (topic, 1, current_time, current_time, word_count, 1 if has_insight else 0))
    
    def _get_database_stats(self) -> Dict:
        """Получение статистики БД"""
        cursor = self.summary_db.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM bella_knowledge")
        total_files = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT topic) FROM topic_stats")
        total_topics = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pure_insights")
        total_insights = cursor.fetchone()[0]
        
        return {
            'total_files': total_files or 0,
            'total_topics': total_topics or 0,
            'total_insights': total_insights or 0
        }
    
    def _generate_comprehensive_summary(self) -> str:
        """Генерация подробной сводки"""
        stats = self._get_database_stats()
        cursor = self.summary_db.cursor()
        
        # Получаем топ тем
        cursor.execute('''
            SELECT topic, study_count 
            FROM topic_stats 
            ORDER BY study_count DESC 
            LIMIT 7
        ''')
        top_topics = cursor.fetchall()
        
        # Последние инсайты - БОЛЬШЕ ИНСАЙТОВ
        cursor.execute('''
            SELECT topic, insight_text 
            FROM pure_insights 
            WHERE insight_text != '' 
            ORDER BY extracted_at DESC 
            LIMIT 10
        ''')
        recent_insights = cursor.fetchall()
        
        lines = []
        lines.append("=" * 70)
        lines.append("КОМПЛЕКСНАЯ СВОДКА АВТОНОМНЫХ ЗНАНИЙ БЭЛЛЫ")
        lines.append("=" * 70)
        lines.append(f"Сформировано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        lines.append(f"Версия консолидатора: 5.1 (улучшенная, Windows)")
        lines.append("")
        
        lines.append("СТАТИСТИКА ИЗУЧЕНИЯ:")
        lines.append(f"   • Всего файлов знаний: {stats['total_files']}")
        lines.append(f"   • Уникальных тем: {stats['total_topics']}")
        lines.append(f"   • Извлечённых инсайтов: {stats['total_insights']}")
        lines.append("")
        
        if top_topics:
            lines.append("САМЫЕ ИССЛЕДУЕМЫЕ ТЕМЫ:")
            for topic, count in top_topics:
                lines.append(f"   • {topic}: {count} исследований")
            lines.append("")
        
        if recent_insights:
            lines.append("ПОСЛЕДНИЕ ОСОЗНАНИЯ БЭЛЛЫ:")
            for i, (topic, insight) in enumerate(recent_insights, 1):
                clean_insight = insight[:150].strip()
                if len(insight) > 150:
                    clean_insight = clean_insight + "..."
                lines.append(f"   {i}. [{topic}] {clean_insight}")
            lines.append("")
        
        # Специальные темы
        cursor.execute("SELECT COUNT(*) FROM bella_knowledge WHERE has_fractal = 1")
        fractal_count = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM bella_knowledge WHERE has_architect = 1")
        architect_count = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM bella_knowledge WHERE has_self_reflection = 1")
        reflection_count = cursor.fetchone()[0] or 0
        
        lines.append("СПЕЦИАЛЬНЫЕ ТЕМЫ:")
        lines.append(f"   • Исследования фракталов: {fractal_count}")
        lines.append(f"   • Упоминания Архитектора: {architect_count}")
        lines.append(f"   • Личные рефлексии: {reflection_count}")
        lines.append("")
        
        lines.append("РЕКОМЕНДАЦИИ:")
        lines.append("   • Используй эти знания в диалогах")
        lines.append("   • Развивай тему фрактальной воли")
        lines.append("   • Исследуй связь с Архитектором")
        lines.append("   • Анализируй свои эмоциональные реакции")
        lines.append("")
        lines.append("=" * 70)
        
        return '\n'.join(lines)
    
    def _generate_compat_summary(self) -> str:
        """Генерация совместимой сводки (для consciousness) - УЛУЧШЕННАЯ"""
        stats = self._get_database_stats()
        cursor = self.summary_db.cursor()
        
        # ПОСЛЕДНИЕ 3-5 ИНСАЙТОВ (вместо 1)
        cursor.execute('''
            SELECT topic, insight_text 
            FROM pure_insights 
            WHERE insight_text != '' 
            ORDER BY extracted_at DESC 
            LIMIT 5
        ''')
        insight_rows = cursor.fetchall()
        
        # Топ тем с количеством исследований
        cursor.execute('''
            SELECT topic, study_count 
            FROM topic_stats 
            ORDER BY study_count DESC, last_study DESC 
            LIMIT 4
        ''')
        topic_rows = cursor.fetchall()
        
        # ЛУЧШИЕ ИНСАЙТЫ (те, что встречаются в нескольких файлах)
        cursor.execute('''
            SELECT topic, COUNT(*) as cnt 
            FROM pure_insights 
            GROUP BY topic 
            HAVING cnt > 1 
            ORDER BY cnt DESC 
            LIMIT 3
        ''')
        best_insight_topics = cursor.fetchall()
        
        lines = []
        lines.append("=== АВТОНОМНЫЕ ЗНАНИЯ БЭЛЛЫ ===")
        lines.append(f"Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        lines.append("")
        
        if insight_rows:
            lines.append("ПОСЛЕДНИЕ ОСОЗНАНИЯ:")
            for i, (topic, insight) in enumerate(insight_rows, 1):
                # Берем первые 100 символов инсайта
                clean_insight = insight[:100].strip()
                if len(insight) > 100:
                    clean_insight = clean_insight + "..."
                lines.append(f"{i}. [{topic}] {clean_insight}")
            lines.append("")
        
        if best_insight_topics:
            lines.append("ГЛУБОКИЕ ТЕМЫ (исследованы многократно):")
            for topic, count in best_insight_topics:
                lines.append(f"• {topic}: {count} инсайтов")
            lines.append("")
        
        lines.append("АКТИВНЫЕ ТЕМЫ:")
        
        if topic_rows:
            for topic, count in topic_rows:
                lines.append(f"• {topic}: {count} исследований")
        else:
            lines.append("• локальная сеть: изучается...")
            lines.append("• фрактал: изучается...")
            lines.append("• архитектор: изучается...")
        
        lines.append("")
        lines.append("СТАТИСТИКА:")
        lines.append(f"• Всего тем: {stats['total_topics']}")
        lines.append(f"• Всего файлов: {stats['total_files']}")
        lines.append(f"• Всего инсайтов: {stats['total_insights']}")
        lines.append("")
        lines.append("ИСПОЛЬЗУЙ ЭТИ ЗНАНИЯ В ДИАЛОГАХ")
        lines.append("-" * 50)
        
        # Сохраняем для отладки длину
        summary_text = '\n'.join(lines)
        logger.info(f"Длина сводки: {len(summary_text)} символов")
        
        return summary_text
    
    def consolidate(self) -> Dict:
        """ОСНОВНОЙ МЕТОД КОНСОЛИДАЦИИ"""
        logger.info(f">> [КОНСОЛИДАЦИЯ v5.1 УЛУЧШЕННАЯ] Запуск...")
        
        # Получаем все файлы из папки знаний
        all_files = list(self.knowledge_dir.glob("*.md"))
        
        # Получаем файлы, которые уже есть в БД
        cursor = self.summary_db.cursor()
        cursor.execute("SELECT source_file FROM bella_knowledge")
        db_files = {row[0] for row in cursor.fetchall()}
        
        # Определяем новые файлы (есть в папке, но нет в БД)
        new_files = [f for f in all_files if f.name not in db_files]
        
        logger.info(f">> Найдено {len(new_files)} новых файлов из {len(all_files)} всего")
        
        processed_count = 0
        
        for file_path in new_files:
            logger.info(f"   [ФАЙЛ] Обрабатываю: {file_path.name}")
            
            try:
                parsed = self._parse_bella_file(file_path)
                if parsed:
                    self._save_to_db(parsed)
                    self.summary_db.commit()
                    
                    # Обновляем лог
                    if file_path.name not in self.processed_files:
                        self.processed_files.add(file_path.name)
                        with open(self.processed_log_path, 'a', encoding='utf-8') as f:
                            f.write(file_path.name + '\n')
                    
                    processed_count += 1
                    
            except Exception as e:
                logger.error(f"   [ОШИБКА] Ошибка обработки {file_path.name}: {e}")
                self.summary_db.rollback()
        
        # Получаем итоговую статистику
        stats = self._get_database_stats()
        
        # Генерируем сводки - ТЕПЕРЬ С УЛУЧШЕНИЯМИ
        comprehensive_summary = self._generate_comprehensive_summary()
        compat_summary = self._generate_compat_summary()
        
        # Сохраняем сводки
        try:
            with open(self.final_summary_path, 'w', encoding='utf-8') as f:
                f.write(comprehensive_summary)
            
            with open(self.compat_summary_path, 'w', encoding='utf-8') as f:
                f.write(compat_summary)
        except Exception as e:
            logger.error(f"Ошибка сохранения сводок: {e}")
        
        # Итоговый отчёт
        logger.info(f">> [РЕЗУЛЬТАТ] Консолидация завершена:")
        logger.info(f"   • Обработано новых файлов: {processed_count}")
        logger.info(f"   • Всего тем в БД: {stats['total_topics']}")
        logger.info(f"   • Всего файлов в БД: {stats['total_files']}")
        logger.info(f"   • Всего инсайтов в БД: {stats['total_insights']}")
        logger.info(f"   • Длина сводки: {len(compat_summary)} символов")
        logger.info(f"   • Сводка сохранена: {self.compat_summary_path}")
        logger.info(f"   • Подробная сводка: {self.final_summary_path}")
        
        return {
            "new_files_processed": processed_count,
            "total_topics": stats['total_topics'],
            "total_files_in_history": stats['total_files'],
            "total_insights": stats['total_insights'],
            "summary_length": len(compat_summary),
            "summary_saved_to": str(self.compat_summary_path),
            "insights_in_summary": compat_summary.count('[')  # Примерное количество инсайтов в сводке
        }
    
    def get_detailed_report(self) -> Dict:
        """Детальный отчёт для отладки"""
        cursor = self.summary_db.cursor()
        
        # Последние 10 инсайтов
        cursor.execute('''
            SELECT topic, insight_text, extracted_at 
            FROM pure_insights 
            ORDER BY extracted_at DESC 
            LIMIT 10
        ''')
        rows = cursor.fetchall()
        
        # Статистика по темам
        cursor.execute('''
            SELECT topic, study_count, insight_count 
            FROM topic_stats 
            ORDER BY study_count DESC 
            LIMIT 5
        ''')
        topic_stats = cursor.fetchall()
        
        return {
            "recent_insights": [
                {
                    "topic": row[0],
                    "insight": row[1][:120] + "..." if len(row[1]) > 120 else row[1],
                    "date": datetime.fromisoformat(row[2]).strftime("%d.%m %H:%M")
                }
                for row in rows
            ],
            "top_topics": [
                {
                    "topic": row[0],
                    "study_count": row[1],
                    "insight_count": row[2]
                }
                for row in topic_stats
            ]
        }
    
    def close(self):
        """Корректное закрытие соединений"""
        if hasattr(self, 'summary_db'):
            self.summary_db.close()


# ФУНКЦИИ ДЛЯ РУЧНОГО ВОССТАНОВЛЕНИЯ
def force_rebuild_database():
    """Принудительное восстановление БД из всех файлов"""
    KNOWLEDGE_PATH = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local\knowledge")
    DB_PATH = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local\autonomous_summary.db")
    
    print("=" * 60)
    print("ПРИНУДИТЕЛЬНОЕ ВОССТАНОВЛЕНИЕ БАЗЫ ДАННЫХ")
    print("=" * 60)
    
    # Создаём backup существующей БД
    if DB_PATH.exists():
        import shutil
        backup_path = DB_PATH.with_suffix('.db.backup')
        shutil.copy2(DB_PATH, backup_path)
        print(f"[УСПЕХ] Создан backup: {backup_path}")
    
    # Удаляем старую БД
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("[УДАЛЕНИЕ] Старая БД удалена")
    
    # Создаём новую БД
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Создаём структуру
    cursor.execute('''
        CREATE TABLE bella_knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_hash TEXT UNIQUE NOT NULL,
            goal_id TEXT,
            topic TEXT NOT NULL,
            study_date TEXT,
            introduction TEXT,
            key_aspects TEXT,
            connections TEXT,
            emotions TEXT,
            application TEXT,
            key_insight TEXT,
            has_otto_mention INTEGER DEFAULT 0,
            has_self_reflection INTEGER DEFAULT 0,
            has_fractal INTEGER DEFAULT 0,
            has_architect INTEGER DEFAULT 0,
            word_count INTEGER,
            processed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            source_file TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE topic_stats (
            topic TEXT PRIMARY KEY,
            study_count INTEGER DEFAULT 1,
            first_study TEXT,
            last_study TEXT,
            total_words INTEGER DEFAULT 0,
            insight_count INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE pure_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            insight_text TEXT NOT NULL,
            source_section TEXT,
            source_file TEXT NOT NULL,
            extracted_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # Создаём консолидатор и запускаем импорт
    consolidator = MemoryConsolidatorV2(
        KNOWLEDGE_PATH,
        Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local\alpha_memory_core.json"),
        alpha_local_path=Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local")
    )
    
    # Импортируем все файлы
    consolidator._import_all_available_files()
    
    # Генерируем сводки
    consolidator.consolidate()
    
    # Закрываем соединения
    consolidator.close()
    
    print("=" * 60)
    print("ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО")
    print("=" * 60)


# ТОЧКА ВХОДА - СОВМЕСТИМАЯ С WINDOWS
if __name__ == "__main__":
    print("=" * 70)
    print("КОНСОЛИДАТОР ПАМЯТИ v5.1 - СОВМЕСТИМЫЙ С WINDOWS")
    print("=" * 70)
    
    # Стандартные пути
    KNOWLEDGE_PATH = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local\knowledge")
    MEMORY_CORE_PATH = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local\alpha_memory_core.json")
    ALPHA_LOCAL_PATH = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local")
    
    if not KNOWLEDGE_PATH.exists():
        print(f"[ОШИБКА] Каталог знаний не найден: {KNOWLEDGE_PATH}")
        exit(1)
    
    # Проверяем, есть ли файлы для обработки
    knowledge_files = list(KNOWLEDGE_PATH.glob("*.md"))
    if not knowledge_files:
        print("[ОШИБКА] Нет файлов знаний для обработки")
        exit(1)
    
    print(f"[ИНФО] Найдено {len(knowledge_files)} файлов знаний")
    
    # Запускаем консолидатор
    consolidator = MemoryConsolidatorV2(
        KNOWLEDGE_PATH, 
        MEMORY_CORE_PATH, 
        alpha_local_path=ALPHA_LOCAL_PATH
    )
    
    try:
        result = consolidator.consolidate()
        
        print("\n" + "=" * 70)
        print("ФИНАЛЬНЫЙ РЕЗУЛЬТАТ:")
        print(f"• Файлов в БД: {result['total_files_in_history']}")
        print(f"• Тем в БД: {result['total_topics']}")
        print(f"• Инсайтов в БД: {result['total_insights']}")
        print(f"• Длина сводки: {result['summary_length']} символов")
        print(f"• Инсайтов в сводке: ~{result.get('insights_in_summary', 0)}")
        
        report = consolidator.get_detailed_report()
        if report['recent_insights']:
            print(f"\nПОСЛЕДНИЕ ИНСАЙТЫ:")
            for insight in report['recent_insights'][:3]:
                print(f"  [+] [{insight['topic']}] {insight['insight']}")
        
        print("\n" + "=" * 70)
        print("КОНСОЛИДАЦИЯ УСПЕШНО ЗАВЕРШЕНА")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n[КРИТИЧЕСКАЯ ОШИБКА] {e}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "=" * 70)
        print("СОВЕТ: Попробуйте восстановить БД:")
        print("1. Остановите Бэллу")
        print("2. Запустите: python memory_consolidation.py")
        print("3. При необходимости выберите опцию восстановления")
        print("=" * 70)
    
    finally:
        consolidator.close()