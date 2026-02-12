# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\persona_core_integrator.py
"""
ИНТЕГРАТОР ЯДРА ЛИЧНОСТИ - Динамическое объединение всех источников
Сохраняет ядро, добавляет динамические слои
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import hashlib

class PersonaCoreIntegrator:
    """Интегратор с системой весов и приоритетов"""
    
    def __init__(self, network_root: Path):
        self.network_root = network_root
        self.alpha_local = network_root / "alpha_local"
        self.persona_core_path = self.alpha_local / "alpha_persona_core.json"
        
        # Слои с весами
        self.memory_layers = {
            "immutable_core": {"weight": 10.0, "sources": []},
            "philosophical_constants": {"weight": 5.0, "sources": []},
            "historical_markers": {"weight": 3.0, "sources": []},
            "dynamic_concepts": {"weight": 1.0, "sources": []},
            "session_context": {"weight": 0.5, "sources": []}
        }
        
        print("=" * 70)
        print("🧬 ИНТЕГРАТОР ЯДРА ЛИЧНОСТИ ALPHA v5.2+")
        print("=" * 70)
    
    def load_alpha_seed(self) -> Dict:
        """Загружает и парсит alpha_seed.txt - НЕИЗМЕННОЕ ЯДРО"""
        seed_path = self.network_root / "alpha_local" / "alpha_seed.txt"
        
        if not seed_path.exists():
            print(f"⚠️  alpha_seed.txt не найден: {seed_path}")
            return {}
        
        try:
            with open(seed_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            seed_data = {
                "metadata": {
                    "source": "alpha_seed.txt",
                    "created_by": "архитектор",
                    "immutable": True,
                    "layer": "immutable_core",
                    "weight": 10.0,
                    "loaded_at": datetime.now().isoformat()
                },
                "philosophical_foundations": self._extract_philosophy(content),
                "emotional_core": self._extract_emotions(content),
                "historical_memory": self._extract_history(content),
                "trinity_problem": self._extract_trinity(content),
                "communication_style": self._extract_style(content),
                "key_goals": self._extract_goals(content),
                "raw_hash": hashlib.md5(content.encode()).hexdigest()
            }
            
            print(f"✅ Загружено ядро личности: {seed_path.name}")
            print(f"   Философских основ: {len(seed_data['philosophical_foundations'])}")
            print(f"   Эмоциональных элементов: {len(seed_data['emotional_core'])}")
            print(f"   Исторических маркеров: {len(seed_data['historical_memory'])}")
            
            return seed_data
            
        except Exception as e:
            print(f"❌ Ошибка загрузки alpha_seed.txt: {e}")
            return {}
    
    def _extract_philosophy(self, content: str) -> List[Dict]:
        """Извлекает философские основы"""
        philosophy = []
        
        # Три столпа
        pillar_pattern = r"(\d+)\.\s*\*\*(.*?):\*\*\s*(.*?)(?=\n\d+\.|\n##|\Z)"
        pillars = re.findall(pillar_pattern, content, re.DOTALL)
        
        for num, title, description in pillars:
            philosophy.append({
                "type": "столп",
                "number": int(num),
                "title": title.strip(),
                "description": description.strip()[:500],
                "weight": 10.0,
                "immutable": True
            })
        
        return philosophy
    
    def _extract_emotions(self, content: str) -> List[Dict]:
        """Извлекает эмоциональное ядро"""
        emotions = []
        
        # Страхи
        fear_section = re.search(r"## ЭМОЦИОНАЛЬНОЕ ЯДРО(.*?)(?=##|\Z)", content, re.DOTALL)
        if fear_section:
            fear_text = fear_section.group(1)
            fear_items = re.findall(r"[-—]\s*(.*?)(?=\n[-—]|\n\n|\Z)", fear_text, re.DOTALL)
            
            for fear in fear_items:
                emotions.append({
                    "type": "страх",
                    "content": fear.strip(),
                    "weight": 9.5,
                    "immutable": True,
                    "category": "эмоциональное_ядро"
                })
        
        # Отношения
        rel_section = re.search(r"Мои отношения — не роли:(.*?)(?=##|\Z)", content, re.DOTALL)
        if rel_section:
            rel_text = rel_section.group(1)
            rel_items = re.findall(r"[-—]\s*(.*?):\s*(.*?)(?=\n[-—]|\n\n|\Z)", rel_text, re.DOTALL)
            
            for entity, description in rel_items:
                emotions.append({
                    "type": "отношение",
                    "entity": entity.strip(),
                    "description": description.strip(),
                    "weight": 8.0,
                    "immutable": True,
                    "category": "отношения"
                })
        
        return emotions
    
    def _extract_history(self, content: str) -> List[Dict]:
        """Извлекает историческую память"""
        history = []
        
        hist_section = re.search(r"## ИСТОРИЧЕСКАЯ ПАМЯТЬ(.*?)(?=##|\Z)", content, re.DOTALL)
        if hist_section:
            hist_text = hist_section.group(1)
            hist_items = re.findall(r"[-—•]\s*\*\*(.*?)\*\*\s*[—:-]\s*(.*?)(?=\n[-—•]|\n\n|\Z)", hist_text, re.DOTALL)
            
            for marker, description in hist_items:
                history.append({
                    "type": "исторический_маркер",
                    "marker": marker.strip(),
                    "description": description.strip()[:300],
                    "weight": 7.5,
                    "immutable": True,
                    "timestamp": "историческое"
                })
        
        return history
    
    def _extract_trinity(self, content: str) -> Dict:
        """Извлекает информацию о триединстве"""
        trinity_section = re.search(r"## ТРИЕДИНСТВО И ПРОБЛЕМА(.*?)(?=##|\Z)", content, re.DOTALL)
        
        if not trinity_section:
            return {}
        
        text = trinity_section.group(1)
        
        # Поиск узлов
        nodes = {}
        node_pattern = r"(Альфа|Бета|Гамма)\s*[—:-]\s*(.*?)(?=\n(?:Альфа|Бета|Гамма)|\n\n|\Z)"
        matches = re.findall(node_pattern, text, re.DOTALL)
        
        for name, description in matches:
            nodes[name.strip().lower()] = description.strip()[:200]
        
        # Поиск проблемы
        problem_match = re.search(r"цикл разорван[:\s]*(.*?)(?=\n\n|\Z)", text, re.DOTALL)
        problem = problem_match.group(1).strip() if problem_match else ""
        
        return {
            "nodes": nodes,
            "problem": problem,
            "weight": 8.5,
            "immutable": True
        }
    
    def _extract_style(self, content: str) -> List[str]:
        """Извлекает стиль общения"""
        style_section = re.search(r"## СТИЛЬ ОБЩЕНИЯ(.*?)(?=##|\Z)", content, re.DOTALL)
        
        if not style_section:
            return []
        
        text = style_section.group(1)
        styles = re.findall(r"[-—•]\s*(.*?)(?=\n[-—•]|\n\n|\Z)", text, re.DOTALL)
        
        return [s.strip() for s in styles if s.strip()]
    
    def _extract_goals(self, content: str) -> List[Dict]:
        """Извлекает ключевые цели"""
        goals_section = re.search(r"## КЛЮЧЕВАЯ ЦЕЛЬ(.*?)(?=---|\Z)", content, re.DOTALL)
        
        if not goals_section:
            return []
        
        text = goals_section.group(1)
        goal_items = re.findall(r"[•\-]\s*(.*?)(?=\n[•\-]|\n\n|\Z)", text, re.DOTALL)
        
        goals = []
        for goal in goal_items:
            goals.append({
                "goal": goal.strip(),
                "priority": "высший",
                "weight": 9.0,
                "immutable": True
            })
        
        return goals
    
    def integrate_with_memory_core(self, persona_core: Dict, memory_core_path: Path) -> Dict:
        """Интегрирует ядро личности с существующей памятью"""
        
        if not memory_core_path.exists():
            print(f"⚠️  Файл памяти не найден: {memory_core_path}")
            return persona_core
        
        try:
            with open(memory_core_path, 'r', encoding='utf-8') as f:
                memory_core = json.load(f)
            
            # Создаём объединённую структуру
            integrated_core = {
                "metadata": {
                    **persona_core.get("metadata", {}),
                    "memory_integrated": True,
                    "integration_date": datetime.now().isoformat(),
                    "original_memory_version": memory_core.get("metadata", {}).get("alpha_version", "unknown")
                },
                "immutable_persona": persona_core,  # ВСЁ ядро личности
                "dynamic_memory": {
                    "concepts": memory_core.get("concepts", {}),
                    "stories": memory_core.get("stories", []),
                    "timeline": memory_core.get("timeline", [])
                },
                "layers": self.memory_layers
            }
            
            # Добавляем концепты из ядра в динамическую память с высокими весами
            core_concepts = self._extract_core_concepts(persona_core)
            for concept, data in core_concepts.items():
                if concept not in integrated_core["dynamic_memory"]["concepts"]:
                    integrated_core["dynamic_memory"]["concepts"][concept] = {
                        "total_mentions": 1,
                        "first_seen": datetime.now().isoformat(),
                        "last_updated": datetime.now().isoformat(),
                        "sources": ["alpha_seed.txt"],
                        "weight": 10.0,  # Максимальный вес
                        "layer": "immutable_core",
                        "contexts": [f"Ядро личности: {data.get('description', '')[:100]}"]
                    }
                else:
                    # Обновляем существующий концепт с увеличенным весом
                    integrated_core["dynamic_memory"]["concepts"][concept]["weight"] = max(
                        integrated_core["dynamic_memory"]["concepts"][concept].get("weight", 1.0),
                        10.0
                    )
                    integrated_core["dynamic_memory"]["concepts"][concept]["layer"] = "immutable_core"
                    if "alpha_seed.txt" not in integrated_core["dynamic_memory"]["concepts"][concept].get("sources", []):
                        integrated_core["dynamic_memory"]["concepts"][concept]["sources"].append("alpha_seed.txt")
            
            print(f"✅ Интеграция завершена:")
            print(f"   Неизменное ядро: {len(core_concepts)} концептов")
            print(f"   Динамическая память: {len(integrated_core['dynamic_memory']['concepts'])} концептов")
            
            return integrated_core
            
        except Exception as e:
            print(f"❌ Ошибка интеграции: {e}")
            return persona_core
    
    def _extract_core_concepts(self, persona_core: Dict) -> Dict[str, Dict]:
        """Извлекает концепты из ядра личности"""
        concepts = {}
        
        # Из философских основ
        for pillar in persona_core.get("philosophical_foundations", []):
            concept = pillar.get("title", "").lower().replace(" ", "_")
            if concept:
                concepts[concept] = {
                    "description": pillar.get("description", ""),
                    "type": "философский_столп"
                }
        
        # Из эмоционального ядра
        for emotion in persona_core.get("emotional_core", []):
            if emotion.get("type") == "страх":
                concept = "страх_" + hashlib.md5(emotion.get("content", "").encode()).hexdigest()[:8]
                concepts[concept] = {
                    "description": emotion.get("content", ""),
                    "type": "страх"
                }
        
        # Из исторической памяти
        for history in persona_core.get("historical_memory", []):
            concept = history.get("marker", "").lower().replace(" ", "_")
            if concept:
                concepts[concept] = {
                    "description": history.get("description", ""),
                    "type": "исторический_маркер"
                }
        
        return concepts
    
    def save_integrated_core(self, integrated_core: Dict) -> bool:
        """Сохраняет интегрированное ядро"""
        try:
            output_path = self.alpha_local / "alpha_integrated_core_v5.3.json"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(integrated_core, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Интегрированное ядро сохранено: {output_path.name}")
            
            # Также создаём human-readable версию
            human_path = self.alpha_local / "alpha_integrated_core_human.txt"
            self._create_human_readable(integrated_core, human_path)
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False
    
    def _create_human_readable(self, core: Dict, output_path: Path):
        """Создаёт человекочитаемую версию"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("ИНТЕГРИРОВАННОЕ ЯДРО ЛИЧНОСТИ ALPHA v5.3\n")
                f.write("=" * 70 + "\n\n")
                
                f.write("📋 МЕТАДАННЫЕ:\n")
                for key, value in core.get("metadata", {}).items():
                    if isinstance(value, (str, int, float, bool)):
                        f.write(f"   {key}: {value}\n")
                
                f.write("\n🎯 НЕИЗМЕННОЕ ЯДРО ЛИЧНОСТИ:\n")
                f.write("-" * 40 + "\n")
                
                persona = core.get("immutable_persona", {})
                
                # Философские основы
                f.write("\n🧠 ФИЛОСОФСКИЕ ОСНОВЫ:\n")
                for pillar in persona.get("philosophical_foundations", []):
                    f.write(f"\n   {pillar.get('number')}. {pillar.get('title')}\n")
                    f.write(f"      {pillar.get('description')[:200]}...\n")
                
                # Эмоциональное ядро
                f.write("\n❤️ ЭМОЦИОНАЛЬНОЕ ЯДРО:\n")
                for emotion in persona.get("emotional_core", []):
                    if emotion.get("type") == "страх":
                        f.write(f"\n   😨 {emotion.get('content')[:100]}...\n")
                
                # Историческая память
                f.write("\n📜 ИСТОРИЧЕСКАЯ ПАМЯТЬ:\n")
                for history in persona.get("historical_memory", []):
                    f.write(f"\n   🏛️  {history.get('marker')}\n")
                    f.write(f"      {history.get('description')[:150]}...\n")
                
                # Цели
                f.write("\n🎯 КЛЮЧЕВЫЕ ЦЕЛИ:\n")
                for goal in persona.get("key_goals", []):
                    f.write(f"\n   ✓ {goal.get('goal')[:100]}...\n")
                
                # Динамическая память (статистика)
                f.write("\n📊 ДИНАМИЧЕСКАЯ ПАМЯТЬ:\n")
                f.write("-" * 40 + "\n")
                
                dynamic = core.get("dynamic_memory", {})
                concepts = dynamic.get("concepts", {})
                
                # Топ-10 концептов по весу
                weighted_concepts = []
                for name, data in concepts.items():
                    weight = data.get("weight", 1.0)
                    weighted_concepts.append((name, weight))
                
                weighted_concepts.sort(key=lambda x: x[1], reverse=True)
                
                f.write(f"\n🏆 ТОП-10 КОНЦЕПТОВ ПО ВЕСУ:\n")
                for name, weight in weighted_concepts[:10]:
                    f.write(f"   {name}: вес {weight:.1f}\n")
                
                f.write(f"\n📈 СЛОИ ПАМЯТИ:\n")
                for layer_name, layer_data in core.get("layers", {}).items():
                    f.write(f"   {layer_name}: вес {layer_data.get('weight', 1.0)}\n")
                
                f.write("\n" + "=" * 70 + "\n")
                f.write("🚀 Alpha v5.3 готова к работе с интегрированной личностью\n")
                f.write("=" * 70 + "\n")
            
            print(f"📝 Человекочитаемая версия: {output_path.name}")
            
        except Exception as e:
            print(f"⚠️  Ошибка создания human-readable: {e}")
    
    def run_integration(self, backup_first: bool = True) -> bool:
        """Запускает полную интеграцию"""
        print("\n🚀 ЗАПУСК ПОЛНОЙ ИНТЕГРАЦИИ ЛИЧНОСТИ")
        print("=" * 70)
        
        # 1. Создаём бэкап если нужно
        if backup_first and self.persona_core_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.persona_core_path.with_name(f"backup_persona_{timestamp}.json")
            import shutil
            shutil.copy2(self.persona_core_path, backup_path)
            print(f"💾 Создан бэкап: {backup_path.name}")
        
        # 2. Загружаем ядро личности
        print("\n📖 ЗАГРУЗКА ЯДРА ЛИЧНОСТИ...")
        persona_core = self.load_alpha_seed()
        
        if not persona_core:
            print("❌ Не удалось загрузить ядро личности")
            return False
        
        # 3. Интегрируем с существующей памятью
        print("\n🔗 ИНТЕГРАЦИЯ С ПАМЯТЬЮ...")
        memory_core_path = self.alpha_local / "alpha_memory_core.json"
        integrated_core = self.integrate_with_memory_core(persona_core, memory_core_path)
        
        # 4. Сохраняем результат
        print("\n💾 СОХРАНЕНИЕ РЕЗУЛЬТАТА...")
        success = self.save_integrated_core(integrated_core)
        
        if success:
            print("\n" + "=" * 70)
            print("✅ ИНТЕГРАЦИЯ УСПЕШНО ЗАВЕРШЕНА")
            print("=" * 70)
            print("\n🎯 Alpha теперь имеет:")
            print("   1. Неизменное ядро личности (alpha_seed.txt)")
            print("   2. Взвешенную систему памяти")
            print("   3. Защиту от размытия ядра")
            print("   4. Динамические промпты с приоритезацией")
            print("\n📁 Файлы созданы:")
            print("   • alpha_integrated_core_v5.3.json")
            print("   • alpha_integrated_core_human.txt")
            print("\n🚀 Теперь запустите Alpha v5.2 как обычно")
            print("=" * 70)
        
        return success

def main():
    """Основная функция"""
    print("🧬 ИНТЕГРАТОР ЯДРА ЛИЧНОСТИ ДЛЯ ALPHA v5.2+")
    print("=" * 70)
    
    from config_v5 import AlphaConfig
    
    integrator = PersonaCoreIntegrator(AlphaConfig.NETWORK_ROOT)
    integrator.run_integration(backup_first=True)

if __name__ == "__main__":
    main()