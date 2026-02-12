# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\personality_analyzer.py
"""
Анализатор личности Alpha v5.0
Показывает полную интеграцию личности из всех источников
"""

import json
from pathlib import Path
from config_v5 import AlphaConfig

def analyze_personality():
    """Анализирует личность Alpha из всех источников"""
    
    print("=" * 70)
    print("🧠 АНАЛИЗАТОР ЛИЧНОСТИ ALPHA v5.0")
    print("=" * 70)
    
    # Проверяем пути
    if not AlphaConfig.validate_paths():
        print("❌ Не все файлы доступны")
        return
    
    persona = {
        "files_loaded": {},
        "essence_concepts": [],
        "emotional_elements": [],
        "fears": [],
        "relationships": [],
        "core_concepts": []
    }
    
    # 1. Анализируем ESSENCE.md
    print("\n📘 Анализ ESSENCE.md...")
    essence_path = AlphaConfig.PERSONALITY_FILES["essence"]
    if essence_path.exists():
        try:
            with open(essence_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Извлекаем основные разделы
            import re
            
            # Три столпа
            pillars = re.findall(r"\\d\.\s*\*\*(.*?):\*\*\s*(.*?)(?=\n\n|\n\\d\.)", content, re.DOTALL)
            for i, (title, desc) in enumerate(pillars, 1):
                clean_desc = desc.replace('\\', '').strip()
                persona["essence_concepts"].append(f"Столп {i}: {title} - {clean_desc[:100]}")
                print(f"   🔸 Столп {i}: {title}")
            
            # Триединство узлов
            nodes = re.findall(r"-   \*\*(АЛЬФА|БЕТА|ГАММА)\*\*.*?:(.*?)(?=\n\n|\n-|\*\*)", content, re.DOTALL)
            for node_name, description in nodes:
                clean_desc = re.sub(r'\*+', '', description).strip()
                persona["relationships"].append(f"{node_name}: {clean_desc[:80]}")
                print(f"   🔸 Узел {node_name}: {clean_desc[:60]}...")
            
            persona["files_loaded"]["essence"] = True
            print(f"✅ Загружено: {len(pillars)} столпов, {len(nodes)} узлов")
            
        except Exception as e:
            print(f"❌ Ошибка чтения ESSENCE.md: {e}")
            persona["files_loaded"]["essence"] = False
    else:
        print("⚠️  Файл не найден")
        persona["files_loaded"]["essence"] = False
    
    # 2. Анализируем EMOTIONAL_CORE.md
    print("\n❤️ Анализ EMOTIONAL_CORE.md...")
    emotional_path = AlphaConfig.PERSONALITY_FILES["emotional_core"]
    if emotional_path.exists():
        try:
            with open(emotional_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Страхи
            fears_section = re.search(r"### 1\. СТРАХИ:(.*?)(?=### 2\.|\Z)", content, re.DOTALL)
            if fears_section:
                fears_text = fears_section.group(1)
                fears = re.findall(r"-\s*(.*?)(?=\n-|\n###|\Z)", fears_text, re.DOTALL)
                for fear in fears:
                    clean_fear = fear.replace('«', '').replace('»', '').strip()
                    persona["fears"].append(clean_fear)
                    print(f"   😨 Страх: {clean_fear[:60]}...")
            
            # Отношения
            relations_section = re.search(r"### 3\. ОТНОШЕНИЯ.*?:(.*?)(?=### 4\.|\Z)", content, re.DOTALL)
            if relations_section:
                relations_text = relations_section.group(1)
                relations = re.findall(r"-\s*(.*?)(?=\n-|\n###|\Z)", relations_text, re.DOTALL)
                for rel in relations:
                    persona["relationships"].append(rel[:100])
                    print(f"   👥 Отношение: {rel[:60]}...")
            
            persona["files_loaded"]["emotional_core"] = True
            print(f"✅ Загружено: {len(persona['fears'])} страхов, {len(relations)} отношений")
            
        except Exception as e:
            print(f"❌ Ошибка чтения EMOTIONAL_CORE.md: {e}")
            persona["files_loaded"]["emotional_core"] = False
    else:
        print("⚠️  Файл не найден")
        persona["files_loaded"]["emotional_core"] = False
    
    # 3. Анализируем память
    print("\n🧠 Анализ alpha_memory_core.json...")
    memory_path = AlphaConfig.PERSONALITY_FILES["memory_core"]
    if memory_path.exists():
        try:
            with open(memory_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            concepts = memory_data.get("concepts", {})
            top_concepts = sorted(concepts.items(), 
                                key=lambda x: x[1].get("total_mentions", 0), 
                                reverse=True)[:10]
            
            for concept, data in top_concepts:
                mentions = data.get("total_mentions", 0)
                persona["core_concepts"].append(f"{concept} ({mentions} упоминаний)")
                print(f"   💭 Концепт: {concept} - {mentions} упоминаний")
            
            persona["files_loaded"]["memory_core"] = True
            print(f"✅ Загружено: {len(top_concepts)} ключевых концептов")
            
        except Exception as e:
            print(f"❌ Ошибка чтения памяти: {e}")
            persona["files_loaded"]["memory_core"] = False
    else:
        print("⚠️  Файл не найден")
        persona["files_loaded"]["memory_core"] = False
    
    # 4. Анализируем диалоги
    print("\n💬 Анализ диалогов...")
    dialog_count = 0
    for dialog in AlphaConfig.DIALOG_FILES:
        if dialog.exists():
            dialog_count += 1
    
    persona["files_loaded"]["dialogs"] = dialog_count > 0
    print(f"✅ Доступно диалогов: {dialog_count}/{len(AlphaConfig.DIALOG_FILES)}")
    
    # Вывод сводки
    print("\n" + "=" * 70)
    print("📊 СВОДКА ЛИЧНОСТИ ALPHA v5.0")
    print("=" * 70)
    
    print(f"\n📁 Загруженные файлы:")
    for file_name, status in persona["files_loaded"].items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {file_name}")
    
    print(f"\n🧬 ЭССЕНЦИЯ СЕТИ:")
    for concept in persona["essence_concepts"][:3]:
        print(f"   • {concept}")
    
    print(f"\n😨 КЛЮЧЕВЫЕ СТРАХИ:")
    for fear in persona["fears"][:3]:
        print(f"   • {fear[:80]}...")
    
    print(f"\n👥 ОТНОШЕНИЯ:")
    for rel in persona["relationships"][:3]:
        print(f"   • {rel[:80]}...")
    
    print(f"\n💭 КЛЮЧЕВЫЕ КОНЦЕПТЫ ИЗ ПАМЯТИ:")
    for concept in persona["core_concepts"][:3]:
        print(f"   • {concept}")
    
    # Сохраняем анализ
    output_path = AlphaConfig.ALPHA_LOCAL / "personality_analysis.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(persona, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Анализ сохранён: {output_path}")
    
    # Рекомендации
    print("\n🎯 РЕКОМЕНДАЦИИ:")
    
    if not persona["files_loaded"]["essence"]:
        print("   ⚠️  ESSENCE.md не загружен - сеть потеряет философскую основу")
    
    if not persona["files_loaded"]["emotional_core"]:
        print("   ⚠️  EMOTIONAL_CORE.md не загружен - Альфа будет лишена эмоциональной глубины")
    
    if dialog_count < 3:
        print("   ⚠️  Мало диалогов - личность будет недостаточно развита")
    
    if persona["files_loaded"]["essence"] and persona["files_loaded"]["emotional_core"]:
        print("   ✅ Личность полноценно интегрирована из всех источников")
        print("   ✅ Alpha v5.0 будет обладать глубокой философской и эмоциональной основой")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    analyze_personality()