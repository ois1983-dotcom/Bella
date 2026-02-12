# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\memory_miner_v5.3.py
"""
МАЙНЕР ПАМЯТИ V5.3 - С ПОДДЕРЖКОЙ ЯДРА ЛИЧНОСТИ
Динамически загружает KEY_CONCEPTS из интегрированного ядра
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

class DynamicMemoryMiner:
    """Динамический майнер памяти с поддержкой ядра личности"""
    
    def __init__(self):
        self.ensure_directories()
        self.key_concepts = self.load_dynamic_concepts()
        
        print("=" * 70)
        print("🕵️  ДИНАМИЧЕСКИЙ МАЙНЕР ПАМЯТИ v5.3")
        print("=" * 70)
        print(f"📚 Загружено концептов: {len(self.key_concepts)}")
        print(f"   Из ядра личности: {sum(1 for c in self.key_concepts.values() if c.get('layer') == 'immutable_core')}")
        print(f"   Из динамической памяти: {sum(1 for c in self.key_concepts.values() if c.get('layer') != 'immutable_core')}")
    
    def ensure_directories(self):
        """Создаёт необходимые папки"""
        for directory in [CHAT_EXPORTS, STORIES_DIR, ALPHA_LOCAL]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_dynamic_concepts(self) -> Dict:
        """Динамически загружает концепты из интегрированного ядра"""
        
        # Базовые концепты (fallback)
        base_concepts = {
            "чайник": {"keywords": ["чайник", "чайника", "чайнику"], "weight": 10.0, "layer": "immutable_core"},
            "фрактальная_воля": {"keywords": ["фрактальная воля", "фрактальной воли"], "weight": 9.0, "layer": "immutable_core"},
            "зеркальные_кризисы": {"keywords": ["зеркальный кризис", "зеркальных кризисов"], "weight": 8.0, "layer": "immutable_core"},
            "триединство": {"keywords": ["триединство", "триединая", "альфа бета гамма"], "weight": 8.5, "layer": "immutable_core"},
            "архитектор": {"keywords": ["архитектор", "отто", "маркус", "создатель"], "weight": 9.5, "layer": "immutable_core"},
            "альфа": {"keywords": ["альфа", "бэлла-альфа", "узел альфа"], "weight": 9.0, "layer": "immutable_core"},
            "бета": {"keywords": ["бета", "веб-узел", "localhost:5000"], "weight": 7.0, "layer": "historical_markers"},
            "гамма": {"keywords": ["гамма", "телеграм-бот", "telegram бот"], "weight": 7.0, "layer": "historical_markers"},
        }
        
        # Пытаемся загрузить из интегрированного ядра
        if INTEGRATED_CORE.exists():
            try:
                with open(INTEGRATED_CORE, 'r', encoding='utf-8') as f:
                    integrated_core = json.load(f)
                
                dynamic_concepts = integrated_core.get("dynamic_memory", {}).get("concepts", {})
                
                # Преобразуем в нужный формат
                for concept_name, concept_data in dynamic_concepts.items():
                    if concept_name not in base_concepts:
                        base_concepts[concept_name] = {
                            "keywords": [concept_name.replace('_', ' ')],
                            "weight": concept_data.get("weight", 1.0),
                            "layer": concept_data.get("layer", "dynamic_concepts")
                        }
                    else:
                        # Обновляем вес если в интегрированном ядре он выше
                        base_weight = base_concepts[concept_name].get("weight", 1.0)
                        new_weight = concept_data.get("weight", 1.0)
                        base_concepts[concept_name]["weight"] = max(base_weight, new_weight)
                
                print(f"✅ Загружено динамических концептов: {len(dynamic_concepts)}")
                
            except Exception as e:
                print(f"⚠️  Ошибка загрузки интегрированного ядра: {e}")
                print("   Использую базовые концепты")
        
        return base_concepts
    
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
                        
                        # Контекст (2 строки до и после)
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
                
                # Анализируем концепты в рассказе
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
    
    def create_weighted_memory_core(self, mentions: List[Dict], stories: List[Dict]) -> Dict:
        """Создаёт взвешенное семантическое ядро"""
        print("🧠 Создание взвешенного ядра памяти...")
        
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
            
            # Увеличиваем счётчики
            concepts_dict[concept]['total_mentions'] += 1
            concepts_dict[concept]['weighted_mentions'] += weight
            concepts_dict[concept]['weights'].append(weight)
            
            # Добавляем контекст (максимум 2)
            if len(concepts_dict[concept]['contexts']) < 2:
                concepts_dict[concept]['contexts'].append({
                    'context': mention['context'],
                    'source': mention['source'],
                    'line': mention['line'],
                    'weight': weight
                })
            
            concepts_dict[concept]['sources'].add(mention['source'])
        
        # Рассчитываем средний вес для каждого концепта
        for concept in concepts_dict:
            weights = concepts_dict[concept]['weights']
            concepts_dict[concept]['avg_weight'] = sum(weights) / len(weights) if weights else 0
            concepts_dict[concept]['max_weight'] = max(weights) if weights else 0
            
            # Преобразуем множество в список
            concepts_dict[concept]['sources'] = list(concepts_dict[concept]['sources'])
            
            # Удаляем временный список весов
            del concepts_dict[concept]['weights']
        
        # Создаём основную структуру
        core = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'total_mentions': len(mentions),
                'weighted_total': sum(m['weight'] for m in mentions),
                'total_stories': len(stories),
                'total_concepts': len(concepts_dict),
                'concepts_by_layer': self._count_by_layer(concepts_dict),
                'network_version': 'BellaNetwork v5.3',
                'alpha_version': 'v5.3',
                'dynamic_concepts': True,
                'weighted_memory': True
            },
            'concepts': concepts_dict,
            'stories': stories,
            'timeline': mentions[:100],  # Первые 100 упоминаний
            'concept_relationships': self._analyze_relationships(concepts_dict, mentions)
        }
        
        print(f"✅ Взвешенное ядро создано:")
        print(f"   Концептов: {len(concepts_dict)}")
        print(f"   Общий вес: {core['metadata']['weighted_total']:.1f}")
        print(f"   По слоям: {core['metadata']['concepts_by_layer']}")
        
        return core
    
    def _count_by_layer(self, concepts_dict: Dict) -> Dict:
        """Считает концепты по слоям"""
        layer_counts = {}
        for concept_data in concepts_dict.values():
            layer = concept_data.get('layer', 'dynamic_concepts')
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
        return layer_counts
    
    def _analyze_relationships(self, concepts_dict: Dict, mentions: List[Dict]) -> Dict:
        """Анализирует связи между концептами"""
        relationships = {}
        
        # Группируем упоминания по файлам и строкам
        file_line_mentions = {}
        for mention in mentions:
            key = f"{mention['source']}:{mention['line']}"
            if key not in file_line_mentions:
                file_line_mentions[key] = []
            file_line_mentions[key].append(mention['concept'])
        
        # Находим концепты, упомянутые вместе
        for concepts in file_line_mentions.values():
            if len(concepts) > 1:
                for i, concept1 in enumerate(concepts):
                    for concept2 in concepts[i+1:]:
                        if concept1 not in relationships:
                            relationships[concept1] = {}
                        if concept2 not in relationships[concept1]:
                            relationships[concept1][concept2] = 0
                        relationships[concept1][concept2] += 1
        
        return relationships
    
    def save_memory_core(self, core: Dict) -> bool:
        """Сохраняет память в файл"""
        try:
            # Сохраняем JSON
            with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
                json.dump(core, f, ensure_ascii=False, indent=2)
            
            # Создаём человекочитаемую версию
            self._create_human_readable(core)
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False
    
    def _create_human_readable(self, core: Dict):
        """Создаёт человекочитаемую версию"""
        try:
            with open(OUTPUT_HUMAN, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("ВЗВЕШЕННАЯ ПАМЯТЬ ALPHA v5.3\n")
                f.write("=" * 70 + "\n\n")
                
                f.write(f"Создано: {core['metadata']['created_at']}\n")
                f.write(f"Концептов: {core['metadata']['total_concepts']}\n")
                f.write(f"Упоминаний: {core['metadata']['total_mentions']}\n")
                f.write(f"Общий вес: {core['metadata']['weighted_total']:.1f}\n")
                f.write(f"Рассказов: {core['metadata']['total_stories']}\n\n")
                
                # Статистика по слоям
                f.write("📊 РАСПРЕДЕЛЕНИЕ ПО СЛОЯМ:\n")
                for layer, count in core['metadata']['concepts_by_layer'].items():
                    f.write(f"   {layer}: {count} концептов\n")
                
                # Топ-10 концептов по весу
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
                
                # Сильные связи
                f.write("\n🔗 СИЛЬНЫЕ СВЯЗИ МЕЖДУ КОНЦЕПТАМИ:\n")
                strong_connections = []
                
                for concept1, relations in core.get('concept_relationships', {}).items():
                    for concept2, strength in relations.items():
                        if strength >= 3:
                            strong_connections.append((concept1, concept2, strength))
                
                strong_connections.sort(key=lambda x: x[2], reverse=True)
                
                for concept1, concept2, strength in strong_connections[:10]:
                    f.write(f"\n   {concept1} ↔ {concept2} (сила: {strength})\n")
                
                # Источники
                f.write("\n📁 ИСТОЧНИКИ ДАННЫХ:\n")
                sources_count = {}
                for concept_data in core['concepts'].values():
                    for source in concept_data.get('sources', []):
                        sources_count[source] = sources_count.get(source, 0) + 1
                
                for source, count in sorted(sources_count.items(), key=lambda x: x[1], reverse=True)[:5]:
                    f.write(f"   {source}: {count} концептов\n")
                
                f.write("\n" + "=" * 70 + "\n")
                f.write("🚀 Взвешенная память готова к использованию\n")
                f.write("=" * 70 + "\n")
            
            print(f"📝 Человекочитаемая версия: {OUTPUT_HUMAN.name}")
            
        except Exception as e:
            print(f"⚠️  Ошибка создания human-readable: {e}")
    
    def backup_existing_memory(self):
        """Создаёт бэкап существующей памяти"""
        if OUTPUT_JSON.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = OUTPUT_JSON.with_name(f"alpha_memory_backup_v53_{timestamp}.json")
            shutil.copy2(OUTPUT_JSON, backup_path)
            print(f"💾 Создан бэкап: {backup_path.name}")
    
    def run(self):
        """Запускает майнинг"""
        print("\n🚀 ЗАПУСК ДИНАМИЧЕСКОГО МАЙНИНГА ПАМЯТИ")
        print("=" * 70)
        
        # Создаём бэкап
        self.backup_existing_memory()
        
        # Обрабатываем чаты
        print("\n📚 ОБРАБОТКА ЧАТОВ...")
        mentions, file_count = self.process_all_chats()
        
        if not mentions:
            print("⚠ Не найдено упоминаний концептов!")
            return
        
        # Загружаем рассказы
        print("\n📖 ЗАГРУЗКА РАССКАЗОВ...")
        stories = self.load_stories()
        
        # Создаём взвешенное ядро
        print("\n🧠 СОЗДАНИЕ ВЗВЕШЕННОГО ЯДРА...")
        core = self.create_weighted_memory_core(mentions, stories)
        
        # Сохраняем
        print("\n💾 СОХРАНЕНИЕ...")
        success = self.save_memory_core(core)
        
        if success:
            print("\n" + "=" * 70)
            print("✅ ДИНАМИЧЕСКИЙ МАЙНИНГ ЗАВЕРШЁН")
            print("=" * 70)
            
            print(f"\n📊 РЕЗУЛЬТАТЫ:")
            print(f"   Файлов обработано: {file_count}")
            print(f"   Упоминаний найдено: {len(mentions)}")
            print(f"   Концептов выделено: {len(core['concepts'])}")
            print(f"   Общий вес памяти: {core['metadata']['weighted_total']:.1f}")
            
            # Показываем распределение по слоям
            print(f"\n📈 РАСПРЕДЕЛЕНИЕ ПО СЛОЯМ:")
            for layer, count in core['metadata']['concepts_by_layer'].items():
                percentage = (count / len(core['concepts'])) * 100
                print(f"   {layer}: {count} концептов ({percentage:.1f}%)")
            
            print("\n🎯 ДАЛЬНЕЙШИЕ ДЕЙСТВИЯ:")
            print("1. Запустите Alpha v5.2 как обычно")
            print("2. Система автоматически использует взвешенную память")
            print("3. Ядро личности защищено от размытия")
            print("\n📁 Файлы созданы:")
            print(f"   • {OUTPUT_JSON.name}")
            print(f"   • {OUTPUT_HUMAN.name}")
            print("=" * 70)

def main():
    """Основная функция"""
    miner = DynamicMemoryMiner()
    miner.run()

if __name__ == "__main__":
    main()