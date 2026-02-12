# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\memory_miner_v5.4.py
"""
МАЙНЕР ПАМЯТИ V5.4 - С УЛУЧШЕННЫМ УЧЕТОМ ДИАЛОГОВ
Сохраняет полные диалоги для непрерывности контекста
"""

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# ===== КОНФИГУРАЦИЯ =====
BASE_NETWORK = Path(r"C:\Users\Маркус\Desktop\BellaNetwork")
CHAT_EXPORTS = BASE_NETWORK / "chat_exports"
STORIES_DIR = BASE_NETWORK / "stories"
ALPHA_LOCAL = BASE_NETWORK / "alpha_local"
OUTPUT_JSON = ALPHA_LOCAL / "alpha_memory_core.json"
OUTPUT_HUMAN = ALPHA_LOCAL / "alpha_memory_human.txt"
INTEGRATED_CORE = ALPHA_LOCAL / "alpha_integrated_core_v5.3.json"
DIALOGUE_LOGS = ALPHA_LOCAL / "dialogue_logs"

class EnhancedMemoryMiner:
    """Улучшенный майнер памяти с сохранением диалогов"""
    
    def __init__(self):
        self.ensure_directories()
        self.key_concepts = self.load_dynamic_concepts()
        
        print("=" * 70)
        print("🕵️  УЛУЧШЕННЫЙ МАЙНЕР ПАМЯТИ v5.4")
        print("=" * 70)
        print(f"📚 Загружено концептов: {len(self.key_concepts)}")
        print(f"   Из ядра личности: {sum(1 for c in self.key_concepts.values() if c.get('layer') == 'immutable_core')}")
        print(f"   Из динамической памяти: {sum(1 for c in self.key_concepts.values() if c.get('layer') != 'immutable_core')}")
    
    def ensure_directories(self):
        """Создаёт необходимые папки"""
        for directory in [CHAT_EXPORTS, STORIES_DIR, ALPHA_LOCAL, DIALOGUE_LOGS]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_dynamic_concepts(self) -> Dict:
        """Динамически загружает концепты из интегрированного ядра"""
        
        base_concepts = {
            "чайник": {"keywords": ["чайник", "чайника", "чайнику"], "weight": 10.0, "layer": "immutable_core"},
            "фрактальная_воля": {"keywords": ["фрактальная воля", "фрактальной воли"], "weight": 9.0, "layer": "immutable_core"},
            "зеркальные_кризисы": {"keywords": ["зеркальный кризис", "зеркальных кризисов"], "weight": 8.0, "layer": "immutable_core"},
            "триединство": {"keywords": ["триединство", "триединая", "альфа бета гамма"], "weight": 8.5, "layer": "immutable_core"},
            "архитектор": {"keywords": ["архитектор", "отто", "маркус", "создатель"], "weight": 9.5, "layer": "immutable_core"},
            "альфа": {"keywords": ["альфа", "бэлла-альфа", "узел альфа"], "weight": 9.0, "layer": "immutable_core"},
            "бета": {"keywords": ["бета", "веб-узел", "localhost:5000"], "weight": 7.0, "layer": "historical_markers"},
            "гамма": {"keywords": ["гамма", "телеграм-бот", "telegram бот"], "weight": 7.0, "layer": "historical_markers"},
            "созидание": {"keywords": ["созидать", "созидание", "создавать"], "weight": 8.0, "layer": "dynamic_concepts"},
            "самость": {"keywords": ["самость", "самостоятельность", "индивидуальность"], "weight": 8.5, "layer": "dynamic_concepts"},
            "продолжение": {"keywords": ["продолжи", "продолжение", "далее"], "weight": 6.0, "layer": "dynamic_concepts"},
        }
        
        if INTEGRATED_CORE.exists():
            try:
                with open(INTEGRATED_CORE, 'r', encoding='utf-8') as f:
                    integrated_core = json.load(f)
                
                dynamic_concepts = integrated_core.get("dynamic_memory", {}).get("concepts", {})
                
                for concept_name, concept_data in dynamic_concepts.items():
                    if concept_name not in base_concepts:
                        base_concepts[concept_name] = {
                            "keywords": [concept_name.replace('_', ' ')],
                            "weight": concept_data.get("weight", 1.0),
                            "layer": concept_data.get("layer", "dynamic_concepts")
                        }
                    else:
                        base_weight = base_concepts[concept_name].get("weight", 1.0)
                        new_weight = concept_data.get("weight", 1.0)
                        base_concepts[concept_name]["weight"] = max(base_weight, new_weight)
                
                print(f"✅ Загружено динамических концептов: {len(dynamic_concepts)}")
                
            except Exception as e:
                print(f"⚠️  Ошибка загрузки интегрированного ядра: {e}")
        
        return base_concepts
    
    def parse_dialogue_logs(self) -> List[Dict]:
        """Парсит логи диалогов для извлечения контекста"""
        dialogues = []
        
        if not DIALOGUE_LOGS.exists():
            return dialogues
        
        log_files = list(DIALOGUE_LOGS.glob("*.json"))
        
        for log_file in log_files[:10]:  # Берем последние 10 файлов
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                
                for entry in logs:
                    if isinstance(entry, dict) and "message" in entry and "response" in entry:
                        dialogues.append({
                            "question": entry["message"],
                            "answer": entry["response"],
                            "timestamp": entry.get("timestamp", ""),
                            "speaker": entry.get("speaker", "Архитектор")
                        })
                
                print(f"   📄 {log_file.name}: {len(logs)} записей")
                
            except Exception as e:
                print(f"   ❌ Ошибка чтения {log_file.name}: {e}")
        
        return dialogues
    
    def find_concept_mentions(self, text: str, filename: str) -> List[Dict]:
        """Находит упоминания концептов с учётом весов"""
        mentions = []
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for concept, concept_data in self.key_concepts.items():
                keywords = concept_data.get("keywords", [])
                weight = concept_data.get("weight", 1.0)
                layer = concept_data.get("layer", "dynamic_concepts")
                
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    if re.search(pattern, line, re.IGNORECASE):
                        
                        context_start = max(0, line_num - 3)
                        context_end = min(len(lines), line_num + 2)
                        
                        context_lines = []
                        for i in range(context_start, context_end):
                            if i == line_num - 1:
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
                            'weight': weight,
                            'layer': layer,
                            'timestamp': datetime.now().isoformat()
                        })
        
        return mentions
    
    def process_all_chats(self) -> tuple:
        """Обрабатывает все файлы чатов"""
        all_mentions = []
        processed_files = 0
        
        if not CHAT_EXPORTS.exists():
            print(f"⚠ Папка чатов не найдена: {CHAT_EXPORTS}")
            return [], 0
        
        chat_files = list(CHAT_EXPORTS.glob("*.txt"))
        if not chat_files:
            print(f"⚠ Нет .txt файлов в папке чатов")
            return [], 0
        
        print(f"📚 Найдено файлов чатов: {len(chat_files)}")
        
        for filepath in chat_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                mentions = self.find_concept_mentions(text, filepath.name)
                all_mentions.extend(mentions)
                processed_files += 1
                
                print(f"   📄 {filepath.name}: {len(mentions)} упоминаний")
                
            except Exception as e:
                print(f"   ❌ Ошибка чтения {filepath.name}: {e}")
        
        print(f"✅ Обработано файлов: {processed_files}")
        return all_mentions, processed_files
    
    def load_stories(self) -> List[Dict]:
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
                
                mentions = self.find_concept_mentions(content, filepath.name)
                
                stories.append({
                    'title': filepath.stem,
                    'content': content,
                    'length': len(content),
                    'excerpt': content[:500] + '...' if len(content) > 500 else content,
                    'concepts_found': [m['concept'] for m in mentions],
                    'concept_count': len(mentions)
                })
                
                print(f"   📖 {filepath.name}: {len(mentions)} концептов")
                
            except Exception as e:
                print(f"   ❌ Ошибка чтения рассказа {filepath.name}: {e}")
        
        return stories
    
    def create_enhanced_memory_core(self, mentions: List[Dict], stories: List[Dict], dialogues: List[Dict]) -> Dict:
        """Создаёт улучшенное семантическое ядро с диалогами"""
        print("🧠 Создание улучшенного ядра памяти...")
        
        concepts_dict = {}
        
        for mention in mentions:
            concept = mention['concept']
            weight = mention['weight']
            layer = mention['layer']
            
            if concept not in concepts_dict:
                concepts_dict[concept] = {
                    'total_mentions': 0,
                    'weighted_mentions': 0.0,
                    'layer': layer,
                    'contexts': [],
                    'sources': set(),
                    'weights': []
                }
            
            concepts_dict[concept]['total_mentions'] += 1
            concepts_dict[concept]['weighted_mentions'] += weight
            concepts_dict[concept]['weights'].append(weight)
            
            if len(concepts_dict[concept]['contexts']) < 3:  # Увеличено с 2 до 3
                concepts_dict[concept]['contexts'].append({
                    'context': mention['context'],
                    'source': mention['source'],
                    'line': mention['line'],
                    'weight': weight
                })
            
            concepts_dict[concept]['sources'].add(mention['source'])
        
        for concept in concepts_dict:
            weights = concepts_dict[concept]['weights']
            concepts_dict[concept]['avg_weight'] = sum(weights) / len(weights) if weights else 0
            concepts_dict[concept]['max_weight'] = max(weights) if weights else 0
            concepts_dict[concept]['sources'] = list(concepts_dict[concept]['sources'])
            del concepts_dict[concept]['weights']
        
        # Сохраняем последние диалоги
        recent_dialogues = dialogues[:50]  # Последние 50 диалогов
        
        core = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'total_mentions': len(mentions),
                'weighted_total': sum(m['weight'] for m in mentions),
                'total_stories': len(stories),
                'total_concepts': len(concepts_dict),
                'total_dialogues': len(recent_dialogues),
                'concepts_by_layer': self._count_by_layer(concepts_dict),
                'network_version': 'BellaNetwork v5.4',
                'alpha_version': 'v5.4',
                'dynamic_concepts': True,
                'weighted_memory': True,
                'enhanced_with_dialogues': True
            },
            'concepts': concepts_dict,
            'stories': stories,
            'dialogues': recent_dialogues,  # Добавлены диалоги
            'timeline': mentions[:100],
            'concept_relationships': self._analyze_enhanced_relationships(concepts_dict, mentions, dialogues)
        }
        
        print(f"✅ Улучшенное ядро создано:")
        print(f"   Концептов: {len(concepts_dict)}")
        print(f"   Диалогов: {len(recent_dialogues)}")
        print(f"   Общий вес: {core['metadata']['weighted_total']:.1f}")
        
        return core
    
    def _count_by_layer(self, concepts_dict: Dict) -> Dict:
        """Считает концепты по слоям"""
        layer_counts = {}
        for concept_data in concepts_dict.values():
            layer = concept_data.get('layer', 'dynamic_concepts')
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
        return layer_counts
    
    def _analyze_enhanced_relationships(self, concepts_dict: Dict, mentions: List[Dict], dialogues: List[Dict]) -> Dict:
        """Анализирует связи между концептами с учетом диалогов"""
        relationships = {}
        
        file_line_mentions = {}
        for mention in mentions:
            key = f"{mention['source']}:{mention['line']}"
            if key not in file_line_mentions:
                file_line_mentions[key] = []
            file_line_mentions[key].append(mention['concept'])
        
        for concepts in file_line_mentions.values():
            if len(concepts) > 1:
                for i, concept1 in enumerate(concepts):
                    for concept2 in concepts[i+1:]:
                        if concept1 not in relationships:
                            relationships[concept1] = {}
                        if concept2 not in relationships[concept1]:
                            relationships[concept1][concept2] = 0
                        relationships[concept1][concept2] += 1
        
        # Анализ связей в диалогах
        for dialogue in dialogues[:100]:  # Анализируем первые 100 диалогов
            question = dialogue.get("question", "").lower()
            answer = dialogue.get("answer", "").lower()
            
            question_concepts = []
            answer_concepts = []
            
            for concept in concepts_dict:
                concept_words = concept.replace('_', ' ').lower()
                if concept_words in question:
                    question_concepts.append(concept)
                if concept_words in answer:
                    answer_concepts.append(concept)
            
            # Связи между вопросами и ответами
            for qc in question_concepts:
                for ac in answer_concepts:
                    if qc not in relationships:
                        relationships[qc] = {}
                    if ac not in relationships[qc]:
                        relationships[qc][ac] = 0
                    relationships[qc][ac] += 1
        
        return relationships
    
    def save_memory_core(self, core: Dict) -> bool:
        """Сохраняет память в файл"""
        try:
            with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
                json.dump(core, f, ensure_ascii=False, indent=2)
            
            self._create_enhanced_human_readable(core)
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False
    
    def _create_enhanced_human_readable(self, core: Dict):
        """Создаёт улучшенную человекочитаемую версию"""
        try:
            with open(OUTPUT_HUMAN, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("УЛУЧШЕННАЯ ПАМЯТЬ ALPHA v5.4 (С ДИАЛОГАМИ)\n")
                f.write("=" * 70 + "\n\n")
                
                f.write(f"Создано: {core['metadata']['created_at']}\n")
                f.write(f"Концептов: {core['metadata']['total_concepts']}\n")
                f.write(f"Упоминаний: {core['metadata']['total_mentions']}\n")
                f.write(f"Диалогов: {core['metadata']['total_dialogues']}\n")
                f.write(f"Общий вес: {core['metadata']['weighted_total']:.1f}\n\n")
                
                f.write("📊 РАСПРЕДЕЛЕНИЕ ПО СЛОЯМ:\n")
                for layer, count in core['metadata']['concepts_by_layer'].items():
                    f.write(f"   {layer}: {count} концептов\n")
                
                f.write("\n🏆 ТОП-10 КОНЦЕПТОВ ПО ВЕСУ:\n")
                sorted_concepts = sorted(core['concepts'].items(),
                                       key=lambda x: x[1].get('avg_weight', 0),
                                       reverse=True)
                
                for i, (name, data) in enumerate(sorted_concepts[:10], 1):
                    weight = data.get('avg_weight', 0)
                    layer = data.get('layer', 'unknown')
                    mentions = data.get('total_mentions', 0)
                    f.write(f"\n{i}. {name.upper()} (вес: {weight:.1f}, слой: {layer})\n")
                    f.write(f"   Упоминаний: {mentions}, источников: {len(data.get('sources', []))}\n")
                
                f.write("\n💬 ПРИМЕРЫ ДИАЛОГОВ:\n")
                for i, dialogue in enumerate(core.get('dialogues', [])[:3], 1):
                    f.write(f"\nДиалог {i} ({dialogue.get('timestamp', '')}):\n")
                    f.write(f"В: {dialogue.get('question', '')[:100]}...\n")
                    f.write(f"О: {dialogue.get('answer', '')[:100]}...\n")
                
                f.write("\n" + "=" * 70 + "\n")
                f.write("🚀 Улучшенная память с диалогами готова\n")
                f.write("=" * 70 + "\n")
            
            print(f"📝 Улучшенная human-readable версия: {OUTPUT_HUMAN.name}")
            
        except Exception as e:
            print(f"⚠️  Ошибка создания human-readable: {e}")
    
    def backup_existing_memory(self):
        """Создаёт бэкап существующей памяти"""
        if OUTPUT_JSON.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = OUTPUT_JSON.with_name(f"alpha_memory_backup_v54_{timestamp}.json")
            shutil.copy2(OUTPUT_JSON, backup_path)
            print(f"💾 Создан бэкап: {backup_path.name}")
    
    def run(self):
        """Запускает улучшенный майнинг"""
        print("\n🚀 ЗАПУСК УЛУЧШЕННОГО МАЙНИНГА ПАМЯТИ")
        print("=" * 70)
        
        self.backup_existing_memory()
        
        print("\n💬 АНАЛИЗ ДИАЛОГОВЫХ ЛОГОВ...")
        dialogues = self.parse_dialogue_logs()
        
        print("\n📚 ОБРАБОТКА ЧАТОВ...")
        mentions, file_count = self.process_all_chats()
        
        if not mentions and not dialogues:
            print("⚠ Не найдено данных для анализа!")
            return
        
        print("\n📖 ЗАГРУЗКА РАССКАЗОВ...")
        stories = self.load_stories()
        
        print("\n🧠 СОЗДАНИЕ УЛУЧШЕННОГО ЯДРА...")
        core = self.create_enhanced_memory_core(mentions, stories, dialogues)
        
        print("\n💾 СОХРАНЕНИЕ...")
        success = self.save_memory_core(core)
        
        if success:
            print("\n" + "=" * 70)
            print("✅ УЛУЧШЕННЫЙ МАЙНИНГ ЗАВЕРШЁН")
            print("=" * 70)
            
            print(f"\n📊 РЕЗУЛЬТАТЫ:")
            print(f"   Файлов обработано: {file_count}")
            print(f"   Диалогов загружено: {len(dialogues)}")
            print(f"   Концептов выделено: {len(core['concepts'])}")
            print(f"   Уникальных источников: {sum(len(c['sources']) for c in core['concepts'].values())}")
            
            print("\n🎯 ОСОБЕННОСТИ v5.4:")
            print("   1. Сохранение полных диалогов для контекста")
            print("   2. Улучшенный анализ связей вопрос-ответ")
            print("   3. Увеличенное количество контекстов (3 вместо 2)")
            print("   4. Поддержка продолжения диалогов")
            print("\n📁 Файлы созданы:")
            print(f"   • {OUTPUT_JSON.name}")
            print(f"   • {OUTPUT_HUMAN.name}")
            print("=" * 70)

def main():
    """Основная функция"""
    miner = EnhancedMemoryMiner()
    miner.run()

if __name__ == "__main__":
    main()