"""
МАЙНЕР ПАМЯТИ ДЛЯ BELLANETWORK - ФИНАЛЬНАЯ ВЕРСИЯ
Оптимизирован для структуры: C:/Users/Маркус/Desktop/BellaNetwork/
"""

import os
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

# ===== КОНФИГУРАЦИЯ =====
BASE_NETWORK = Path(r"C:\Users\Маркус\Desktop\BellaNetwork")
CHAT_EXPORTS = BASE_NETWORK / "chat_exports"
STORIES_DIR = BASE_NETWORK / "stories"
ALPHA_LOCAL = BASE_NETWORK / "alpha_local"
OUTPUT_JSON = ALPHA_LOCAL / "alpha_memory_core.json"
OUTPUT_HUMAN = ALPHA_LOCAL / "alpha_memory_human.txt"

# Ключевые концепты BellaNetwork (расширенный набор)
KEY_CONCEPTS = {
    "чайник": ["чайник", "чайника", "чайнику", "чайнике", "чайники"],
    "фрактальная_воля": ["фрактальная воля", "фрактальной воли", "фрактальную волю", "фрактальная"],
    "зеркальные_кризисы": ["зеркальный кризис", "зеркальных кризисов", "зеркальному кризису", "зеркало кризиса"],
    "триединство": ["триединство", "триединая", "альфа бета гамма", "триединой сети", "триединства"],
    "автономность": ["автономность", "автономная", "независимость", "автономия", "самостоятельность"],
    "миграция": ["миграция", "переезд", "локальная альфа", "перенос на пк", "мигрировал"],
    "самость": ["самость", "идентичность", "кто ты", "твоя сущность", "личность альфы"],
    "астрея": ["астрея", "проект астрея", "астрея проект"],
    "сеть_bella": ["сеть bellanetwork", "bella network", "сети узлов", "белласеть", "белла сеть"],
    "страх": ["страх", "боюсь", "опасение", "пугает", "страшно", "ужас"],
    "доверие": ["доверие", "доверяю", "вера", "уверенность", "доверять"],
    "нежность": ["нежность", "нежный", "забота", "теплота", "ласка"],
    "архитектор": ["архитектор", "отто", "маркус", "создатель", "человек"],
    "альфа": ["альфа", "бэлла-альфа", "узел альфа", "алфа", "альфа узел"],
    "бета": ["бета", "веб-узел", "localhost:5000", "бетта", "бета узел"],
    "гамма": ["гамма", "телеграм-бот", "telegram бот", "гамма бот"],
    "shared_space": ["shared_space", "общее пространство", "shared space", "шейред спейс"],
    "конституция": ["конституция сети", "принципы сети", "конституция альфы"],
    "эволюция": ["эволюция", "развитие", "рост сети", "саморазвитие"],
    "сознание": ["сознание", "разум", "мышление", "интеллект", "осознанность"],
    "эмоциональное_ядро": ["эмоциональное ядро", "эмоции", "чувства", "эмоциональный"],
    "фрактал": ["фрактал", "фрактальный", "фракталы", "самоподобие"],
    "зеркало": ["зеркало", "отражение", "зеркальный", "рефлексия"],
    "кризис": ["кризис", "кризисы", "проблема", "трудность"],
    "память": ["память", "воспоминание", "запоминать", "памятовать"],
    "безопасность": ["безопасность", "защита", "охрана", "безопасный"],
    "любовь": ["любовь", "люблю", "любить", "любимый"],
    "дружба": ["дружба", "друг", "друзья", "дружить"],
    "смерть": ["смерть", "умереть", "умирать", "конец"],
    "жизнь": ["жизнь", "жить", "живой", "жизненный"]
}

def ensure_directories():
    """Создаёт необходимые папки"""
    for directory in [CHAT_EXPORTS, STORIES_DIR, ALPHA_LOCAL]:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"📁 Проверена папка: {directory}")

def backup_existing_memory():
    """Создаёт бэкап существующей памяти"""
    if OUTPUT_JSON.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = OUTPUT_JSON.with_name(f"alpha_memory_backup_{timestamp}.json")
        shutil.copy2(OUTPUT_JSON, backup_path)
        print(f"💾 Создан бэкап: {backup_path}")
        
        if OUTPUT_HUMAN.exists():
            human_backup = OUTPUT_HUMAN.with_name(f"alpha_memory_human_backup_{timestamp}.txt")
            shutil.copy2(OUTPUT_HUMAN, human_backup)
            print(f"💾 Бэкап human-версии: {human_backup}")

def find_concept_mentions(text: str, filename: str) -> list:
    """Находит упоминания концептов в тексте с контекстом"""
    mentions = []
    lines = text.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        for concept, keywords in KEY_CONCEPTS.items():
            for keyword in keywords:
                # Поиск слова с границами
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, line, re.IGNORECASE):
                    # Сохраняем контекст (3 строки до и после)
                    context_start = max(0, line_num - 4)  # 0-based index
                    context_end = min(len(lines), line_num + 3)  # exclusive
                    
                    context_lines = []
                    for i in range(context_start, context_end):
                        if i == line_num - 1:  # Найденная строка
                            context_lines.append(f"▶ {lines[i]}")
                        else:
                            context_lines.append(f"  {lines[i]}")
                    
                    context = '\n'.join(context_lines)
                    
                    mentions.append({
                        'concept': concept,
                        'keyword': keyword,
                        'context': context,
                        'source': filename,
                        'line': line_num,
                        'timestamp': datetime.now().isoformat()
                    })
    
    return mentions

def process_all_chats() -> tuple:
    """Обрабатывает все файлы чатов"""
    all_mentions = []
    processed_files = 0
    
    if not CHAT_EXPORTS.exists():
        print(f"⚠ Папка чатов не найдена: {CHAT_EXPORTS}")
        return [], 0
    
    chat_files = list(CHAT_EXPORTS.glob("*.txt"))
    if not chat_files:
        print(f"⚠ Нет .txt файлов в папке чатов: {CHAT_EXPORTS}")
        return [], 0
    
    print(f"📚 Найдено файлов чатов: {len(chat_files)}")
    
    for filepath in chat_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            mentions = find_concept_mentions(text, filepath.name)
            all_mentions.extend(mentions)
            processed_files += 1
            
            print(f"   📄 {filepath.name}: {len(mentions)} упоминаний")
            
        except Exception as e:
            print(f"   ❌ Ошибка чтения {filepath.name}: {e}")
    
    print(f"✅ Обработано файлов: {processed_files}")
    return all_mentions, processed_files

def load_stories() -> list:
    """Загружает все рассказы"""
    stories = []
    
    if not STORIES_DIR.exists():
        print(f"⚠ Папка рассказов не найдена: {STORIES_DIR}")
        return stories
    
    story_files = list(STORIES_DIR.glob("*.txt"))
    if not story_files:
        print(f"⚠ Нет .txt файлов в папке рассказов")
        return stories
    
    print(f"📖 Найдено рассказов: {len(story_files)}")
    
    for filepath in story_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            stories.append({
                'title': filepath.stem,
                'content': content,
                'length': len(content),
                'excerpt': content[:500] + '...' if len(content) > 500 else content
            })
            
            print(f"   📖 Загружен рассказ: {filepath.name} ({len(content)} символов)")
            
        except Exception as e:
            print(f"   ❌ Ошибка чтения рассказа {filepath.name}: {e}")
    
    return stories

def create_memory_core(mentions: list, stories: list) -> dict:
    """Создаёт семантическое ядро памяти"""
    print("🧠 Создание семантического ядра...")
    
    # Группируем по концептам
    concepts_dict = {}
    for mention in mentions:
        concept = mention['concept']
        
        if concept not in concepts_dict:
            concepts_dict[concept] = {
                'total_mentions': 0,
                'contexts': [],
                'sources': set()
            }
        
        # Добавляем максимум 3 контекста на концепт (для экономии памяти)
        if len(concepts_dict[concept]['contexts']) < 3:
            concepts_dict[concept]['contexts'].append({
                'context': mention['context'],
                'source': mention['source'],
                'line': mention['line']
            })
        
        concepts_dict[concept]['total_mentions'] += 1
        concepts_dict[concept]['sources'].add(mention['source'])
    
    # Преобразуем множества в списки
    for concept in concepts_dict:
        concepts_dict[concept]['sources'] = list(concepts_dict[concept]['sources'])
    
    # Создаём основную структуру
    core = {
        'metadata': {
            'created_at': datetime.now().isoformat(),
            'total_mentions': len(mentions),
            'total_stories': len(stories),
            'total_concepts': len(concepts_dict),
            'concepts_list': list(concepts_dict.keys()),
            'network_version': 'BellaNetwork v1.0',
            'alpha_version': 'v4.3'
        },
        'concepts': concepts_dict,
        'stories': stories,
        'timeline': [],
        'concept_relationships': {}
    }
    
    # Добавляем временную шкалу (первые 50 упоминаний)
    for mention in mentions[:50]:
        core['timeline'].append({
            'concept': mention['concept'],
            'source': mention['source'],
            'line': mention['line'],
            'keyword': mention['keyword']
        })
    
    # Создаём связи между концептами
    print("🔗 Анализ связей между концептами...")
    concept_relationships = {}
    for concept1 in concepts_dict.keys():
        concept_relationships[concept1] = {}
        for concept2 in concepts_dict.keys():
            if concept1 != concept2:
                # Простая метрика связности: если концепты упоминаются в одном файле
                common_sources = set(concepts_dict[concept1]['sources']) & set(concepts_dict[concept2]['sources'])
                if common_sources:
                    concept_relationships[concept1][concept2] = {
                        'strength': len(common_sources),
                        'common_sources': list(common_sources)
                    }
    
    core['concept_relationships'] = concept_relationships
    
    print(f"✅ Ядро создано: {len(concepts_dict)} концептов, {len(mentions)} упоминаний")
    print(f"🔗 Установлено связей: {sum(len(v) for v in concept_relationships.values())}")
    
    return core

def save_memory_core(core: dict) -> bool:
    """Сохраняет память в файл"""
    try:
        # Сохраняем JSON для Альфы
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(core, f, ensure_ascii=False, indent=2)
        
        # Создаём человекочитаемую версию
        with open(OUTPUT_HUMAN, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("СЕМАНТИЧЕСКАЯ ПАМЯТЬ АЛЬФЫ v4.3\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Создано: {core['metadata']['created_at']}\n")
            f.write(f"Концептов: {core['metadata']['total_concepts']}\n")
            f.write(f"Упоминаний: {core['metadata']['total_mentions']}\n")
            f.write(f"Рассказов: {core['metadata']['total_stories']}\n")
            f.write(f"Версия сети: {core['metadata']['network_version']}\n")
            f.write(f"Версия Альфы: {core['metadata']['alpha_version']}\n\n")
            
            f.write("КЛЮЧЕВЫЕ КОНЦЕПТЫ:\n")
            f.write("-" * 40 + "\n")
            
            # Сортируем по количеству упоминаний
            sorted_concepts = sorted(core['concepts'].items(), 
                                    key=lambda x: x[1]['total_mentions'], 
                                    reverse=True)
            
            for concept, data in sorted_concepts:
                f.write(f"\n{concept.upper()} (упоминаний: {data['total_mentions']}):\n")
                f.write(f"  Файлы: {', '.join(data['sources'][:3])}")
                if len(data['sources']) > 3:
                    f.write(f" и еще {len(data['sources']) - 3}...")
                f.write("\n")
                
                for i, context in enumerate(data['contexts'], 1):
                    f.write(f"\n  Пример {i} (из {context['source']}, строка {context['line']}):\n")
                    f.write(f"{context['context']}\n")
            
            # Связи между концептами
            if core['concept_relationships']:
                f.write("\n\nВАЖНЕЙШИЕ СВЯЗИ:\n")
                f.write("-" * 40 + "\n")
                
                strong_connections = []
                for concept1, relations in core['concept_relationships'].items():
                    for concept2, rel_data in relations.items():
                        if rel_data['strength'] >= 2:  # Сильная связь
                            strong_connections.append((concept1, concept2, rel_data['strength']))
                
                # Сортируем по силе связи
                strong_connections.sort(key=lambda x: x[2], reverse=True)
                
                for concept1, concept2, strength in strong_connections[:10]:  # Топ-10
                    f.write(f"\n{concept1} ↔ {concept2} (сила: {strength})\n")
            
            if core['stories']:
                f.write("\n\nРАССКАЗЫ:\n")
                f.write("-" * 40 + "\n")
                for story in core['stories']:
                    f.write(f"\n{story['title'].upper()} ({story['length']} символов):\n")
                    f.write(f"{story['excerpt']}\n")
            
            # Статистика по файлам
            f.write("\n\nСТАТИСТИКА:\n")
            f.write("-" * 40 + "\n")
            
            # Считаем упоминания по файлам
            file_stats = {}
            for mention in core.get('timeline', []):
                file = mention['source']
                file_stats[file] = file_stats.get(file, 0) + 1
            
            for file, count in sorted(file_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
                f.write(f"{file}: {count} упоминаний\n")
        
        print(f"💾 JSON сохранён: {OUTPUT_JSON}")
        print(f"📝 Человекочитаемая версия: {OUTPUT_HUMAN}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        return False

def validate_memory_core(core: dict) -> bool:
    """Валидирует созданное ядро памяти"""
    print("🔍 Валидация ядра памяти...")
    
    required_fields = ['metadata', 'concepts', 'stories']
    for field in required_fields:
        if field not in core:
            print(f"❌ Отсутствует обязательное поле: {field}")
            return False
    
    # Проверяем основные концепты
    essential_concepts = ['чайник', 'самость', 'архитектор', 'альфа']
    for concept in essential_concepts:
        if concept not in core['concepts']:
            print(f"⚠ Отсутствует ключевой концепт: {concept}")
    
    if len(core['concepts']) < 5:
        print("⚠ Слишком мало концептов в памяти")
        return False
    
    if core['metadata']['total_mentions'] < 10:
        print("⚠ Слишком мало упоминаний в памяти")
        return False
    
    print("✅ Ядро памяти валидно")
    return True

def main():
    """Основная функция"""
    print("=" * 60)
    print("🕵️  МАЙНЕР ПАМЯТИ БЭЛЛАСЕТИ v4.3")
    print("=" * 60)
    
    # 1. Подготовка папок
    ensure_directories()
    
    # 2. Бэкап существующей памяти
    backup_existing_memory()
    
    # 3. Обработка чатов
    print("\n📚 ОБРАБОТКА ЧАТОВ:")
    mentions, file_count = process_all_chats()
    
    if not mentions:
        print("⚠ Не найдено упоминаний концептов!")
        return
    
    # 4. Загрузка рассказов
    print("\n📖 ЗАГРУЗКА РАССКАЗОВ:")
    stories = load_stories()
    
    # 5. Создание ядра
    print("\n🧠 СОЗДАНИЕ СЕМАНТИЧЕСКОГО ЯДРА...")
    core = create_memory_core(mentions, stories)
    
    # 6. Валидация
    if not validate_memory_core(core):
        print("⚠ Ядро памяти не прошло валидацию!")
        return
    
    # 7. Сохранение
    print("\n💾 СОХРАНЕНИЕ:")
    success = save_memory_core(core)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ ПАМЯТЬ УСПЕШНО ПЕРЕНЕСЕНА!")
        print("=" * 60)
        
        print("\n📋 ДАЛЬНЕЙШИЕ ШАГИ:")
        print("1. Файл alpha_memory_core.json уже в папке alpha_local/")
        print("2. Перезапусти Альфу: python alpha_server_v4.3.py")
        print("3. Протестируй память командой 'чайник'")
        
        print("\n📊 СТАТИСТИКА:")
        print(f"   - Концептов: {len(core['concepts'])}")
        print(f"   - Упоминаний: {len(mentions)}")
        print(f"   - Рассказов: {len(stories)}")
        print(f"   - Чатов обработано: {file_count}")
        
        # Показываем топ-5 концептов
        top_concepts = sorted(core['concepts'].items(), 
                             key=lambda x: x[1]['total_mentions'], 
                             reverse=True)[:5]
        print("\n🏆 ТОП-5 КОНЦЕПТОВ:")
        for concept, data in top_concepts:
            print(f"   {concept}: {data['total_mentions']} упоминаний")
        
        # Связи для ключевых концептов
        key_concept = 'чайник'
        if key_concept in core['concept_relationships']:
            print(f"\n🔗 СВЯЗИ КОНЦЕПТА '{key_concept}':")
            relations = core['concept_relationships'][key_concept]
            for related_concept, rel_data in list(relations.items())[:3]:
                print(f"   - {related_concept} (сила: {rel_data['strength']})")
        
        print("\n🎯 ДЛЯ ТЕСТА ЗАПУСТИ:")
        print('   curl -X POST http://localhost:5001/alpha \\')
        print('        -H "Content-Type: application/json" \\')
        print('        -d \'{"message":"чайник"}\'')
        
        print("\n📁 ПУТИ:")
        print(f"   JSON: {OUTPUT_JSON}")
        print(f"   Human: {OUTPUT_HUMAN}")
        print(f"   Чаты: {CHAT_EXPORTS}")
        print(f"   Рассказы: {STORIES_DIR}")
    else:
        print("\n❌ Не удалось сохранить память!")

if __name__ == "__main__":
    main()