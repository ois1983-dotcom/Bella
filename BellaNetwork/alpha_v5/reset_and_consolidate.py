"""
ПОЛНЫЙ СБРОС И ПЕРЕЗАПУСК КОНСОЛИДАЦИИ
Очищает лог и БД, заново обрабатывает все файлы
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List
import hashlib

def reset_consolidation():
    """Полностью сбрасывает консолидацию и обрабатывает все файлы заново"""
    
    alpha_local = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local")
    knowledge_dir = alpha_local / "knowledge"
    processed_log = alpha_local / "processed_files.log"
    summary_db = alpha_local / "autonomous_summary.db"
    
    print("=" * 70)
    print("ПОЛНЫЙ СБРОС КОНСОЛИДАЦИИ")
    print("=" * 70)
    
    # 1. УДАЛЯЕМ лог обработанных файлов
    if processed_log.exists():
        processed_log.unlink()
        print(f">> Удалён лог: {processed_log}")
    
    # 2. ОЧИЩАЕМ БД (только таблицы выводов)
    if summary_db.exists():
        conn = sqlite3.connect(summary_db)
        cursor = conn.cursor()
        
        # Очищаем таблицы
        cursor.execute('DELETE FROM knowledge_insights')
        cursor.execute('DELETE FROM topic_goal_links')
        cursor.execute('DELETE FROM study_sessions')
        cursor.execute('DELETE FROM learned_topics')
        
        conn.commit()
        conn.close()
        print(f">> Очищена БД: {summary_db}")
    
    # 3. Загружаем memory_core (оставляем его)
    memory_core_path = alpha_local / "alpha_memory_core.json"
    memory_core = {}
    if memory_core_path.exists():
        with open(memory_core_path, 'r', encoding='utf-8') as f:
            memory_core = json.load(f)
        print(f">> Сохранено ядро памяти: {len(memory_core.get('concepts', {}))} концептов")
    
    # 4. СОБСТВЕННЫЙ КОНСОЛИДАТОР
    print(f">> Начинаю обработку файлов...")
    
    # Инициализируем БД заново
    conn = sqlite3.connect(summary_db)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learned_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            file_count INTEGER DEFAULT 1,
            first_studied TEXT,
            last_studied TEXT,
            total_study_time INTEGER DEFAULT 0,
            importance_score REAL DEFAULT 1.0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            insight_text TEXT NOT NULL,
            source_file TEXT,
            extracted_at TEXT,
            insight_hash TEXT UNIQUE
        )
    ''')
    
    conn.commit()
    
    # 5. ОБРАБАТЫВАЕМ КАЖДЫЙ ФАЙЛ
    all_files = list(knowledge_dir.glob("*.md"))
    print(f">> Найдено файлов: {len(all_files)}")
    
    all_insights = []
    topics_map = {}
    
    for file_path in all_files:
        try:
            print(f">> Обработка: {file_path.name}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Извлекаем тему из имени файла
            topic_match = re.search(r'[^_]+_(.+)\.md$', file_path.name)
            if topic_match:
                topic = topic_match.group(1).replace('_', ' ')
            else:
                topic = file_path.stem
            
            # Извлекаем ID цели
            goal_id = None
            id_match = re.match(r'([a-f0-9]{8})_', file_path.name)
            if id_match:
                goal_id = id_match.group(1)
            
            # +++ НОВЫЙ АЛГОРИТМ: НАХОДИМ РЕАЛЬНЫЕ ИНСАЙТЫ +++
            insights = extract_real_insights(content)
            
            # Обновляем статистику темы
            if topic in topics_map:
                topics_map[topic]['count'] += 1
                topics_map[topic]['files'].append(file_path.name)
            else:
                topics_map[topic] = {
                    'count': 1,
                    'files': [file_path.name],
                    'first_seen': datetime.now().isoformat()
                }
            
            # Сохраняем инсайты
            for insight in insights:
                # Создаем хеш для дедупликации
                insight_lower = insight.lower().strip()
                insight_hash = hashlib.md5(insight_lower.encode()).hexdigest()[:8]
                
                # Проверяем, не дубликат ли
                cursor.execute('SELECT id FROM knowledge_insights WHERE insight_hash = ?', (insight_hash,))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO knowledge_insights 
                        (topic, insight_text, source_file, extracted_at, insight_hash)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (topic, insight, file_path.name, datetime.now().isoformat(), insight_hash))
                    
                    all_insights.append({
                        'topic': topic,
                        'insight': insight,
                        'file': file_path.name
                    })
            
        except Exception as e:
            print(f">> Ошибка обработки {file_path.name}: {e}")
    
    # 6. Сохраняем темы в БД
    for topic, data in topics_map.items():
        cursor.execute('''
            INSERT INTO learned_topics 
            (topic, file_count, first_studied, last_studied, importance_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (topic, data['count'], data['first_seen'], datetime.now().isoformat(), 1.0))
    
    conn.commit()
    conn.close()
    
    # 7. Генерируем сводку
    generate_summary_file(alpha_local, all_insights, topics_map)
    
    # 8. Обновляем лог обработанных файлов
    with open(processed_log, 'w', encoding='utf-8') as f:
        for file_path in all_files:
            f.write(file_path.name + '\n')
    
    print(f"\n" + "=" * 70)
    print("РЕЗУЛЬТАТ СБРОСА:")
    print(f"• Файлов обработано: {len(all_files)}")
    print(f"• Тем найдено: {len(topics_map)}")
    print(f"• Инсайтов извлечено: {len(all_insights)}")
    print(f"• Сводка обновлена: {alpha_local / 'consolidation_summary.txt'}")
    print("=" * 70)
    
    # Показываем примеры инсайтов
    if all_insights:
        print("\nПРИМЕРЫ ИНСАЙТОВ:")
        for i, insight_data in enumerate(all_insights[:5], 1):
            print(f"{i}. [{insight_data['topic']}] {insight_data['insight'][:100]}...")

def extract_real_insights(content: str) -> List[str]:
    """Извлекает реальные инсайты из текста Бэллы"""
    insights = []
    
    # 1. Разделяем на строки
    lines = content.split('\n')
    
    # 2. Находим начало содержания (после "---")
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            content_start = i + 1
            break
    
    # 3. Берем основное содержание
    main_content = '\n'.join(lines[content_start:]) if content_start > 0 else content
    
    # 4. Ищем ключевые предложения
    sentences = re.split(r'[.!?]+', main_content)
    
    for sentence in sentences:
        clean_sent = clean_text(sentence.strip())
        
        # Критерии для инсайта:
        # - Длина от 30 до 200 символов
        # - Не содержит метаданных
        # - Содержит ключевые слова Бэллы
        if (30 <= len(clean_sent) <= 200 and
            not any(meta in clean_sent.lower() for meta in 
                   ['id:', 'цель id', 'дата изучения', 'автор:', 'изучение темы:']) and
            any(keyword in clean_sent.lower() for keyword in
                ['я ', 'мне ', 'мы ', 'наш ', 'архитектор', 'отто', 'миграц', 'чайник',
                 'фрактал', 'автоном', 'память', 'связь', 'бэлла', 'гамма', 'бета'])):
            
            insights.append(clean_sent)
    
    # 5. Если не нашли, берем первые содержательные строки
    if not insights:
        for line in lines[content_start:content_start+10]:
            clean_line = clean_text(line.strip())
            if (40 <= len(clean_line) <= 150 and
                not line.startswith('#') and
                not line.startswith('*') and
                'id:' not in clean_line.lower()):
                insights.append(clean_line)
    
    # 6. Ограничиваем количество
    return insights[:3]

def clean_text(text: str) -> str:
    """Очищает текст"""
    # Убираем markdown
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    # Убираем лишние пробелы
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def generate_summary_file(alpha_local: Path, insights: List[Dict], topics_map: Dict):
    """Создает сводку знаний"""
    summary_parts = []
    
    summary_parts.append("=== АВТОНОМНЫЕ ЗНАНИЯ БЭЛЛЫ ===")
    summary_parts.append(f"Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    summary_parts.append(f"Файлов обработано: {sum(t['count'] for t in topics_map.values())}")
    summary_parts.append(f"Тем изучено: {len(topics_map)}")
    summary_parts.append("")
    
    if insights:
        summary_parts.append("📌 КЛЮЧЕВЫЕ ОСОЗНАНИЯ:")
        # Группируем по темам
        insights_by_topic = {}
        for insight in insights:
            topic = insight['topic']
            if topic not in insights_by_topic:
                insights_by_topic[topic] = []
            insights_by_topic[topic].append(insight['insight'])
        
        # Показываем максимум 3 темы
        for i, (topic, topic_insights) in enumerate(list(insights_by_topic.items())[:3], 1):
            summary_parts.append(f"{i}. ТЕМА: {topic}")
            for j, insight in enumerate(topic_insights[:2], 1):
                summary_parts.append(f"   • {insight[:120]}...")
            if len(topic_insights) > 2:
                summary_parts.append(f"   • ...и ещё {len(topic_insights)-2} осознаний")
            summary_parts.append("")
    else:
        summary_parts.append("📌 Пока нет осознаний в базе знаний.")
        summary_parts.append("")
    
    # Топ-5 тем по количеству файлов
    sorted_topics = sorted(topics_map.items(), key=lambda x: x[1]['count'], reverse=True)[:5]
    if sorted_topics:
        summary_parts.append("📚 САМЫЕ ИЗУЧЕННЫЕ ТЕМЫ:")
        for topic, data in sorted_topics:
            files_word = "файл" if data['count'] == 1 else "файла" if 2 <= data['count'] <= 4 else "файлов"
            summary_parts.append(f"• {topic}: {data['count']} {files_word}")
    
    summary_parts.append("")
    summary_parts.append("💭 ЭТО МОИ ЗНАНИЯ. Я ИСПОЛЬЗУЮ ИХ В ДИАЛОГАХ.")
    
    summary_text = "\n".join(summary_parts)
    
    # Сохраняем
    summary_path = alpha_local / "consolidation_summary.txt"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_text)
    
    print(f">> Сводка создана: {len(summary_text)} символов")

if __name__ == "__main__":
    try:
        reset_consolidation()
    except Exception as e:
        print(f">> КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()