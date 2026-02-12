# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\memory_adapter_v5_enhanced.py
"""
УЛУЧШЕННЫЙ АДАПТЕР ПАМЯТИ V5.4 - С ИНТЕГРАЦИЕЙ ДИАЛОГОВ
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import shutil

class EnhancedMemoryAdapter:
    """
    Улучшенный адаптер с интеграцией диалогов и ядра личности
    """
    
    def __init__(self, alpha_local_path: Path):
        self.alpha_local = Path(alpha_local_path)
        self.memory_core_path = self.alpha_local / "alpha_memory_core.json"
        self.dialogue_logs_dir = self.alpha_local / "dialogue_logs"
        
        print("=" * 60)
        print("🧠 УЛУЧШЕННЫЙ АДАПТЕР ПАМЯТИ V5.4")
        print("=" * 60)
    
    def integrate_dialogues_into_memory(self) -> bool:
        """Интегрирует диалоги из логов в память"""
        print("\n💬 Интеграция диалогов в память...")
        
        if not self.dialogue_logs_dir.exists():
            print("⚠️  Папка с логами диалогов не найдена")
            return False
        
        # Загружаем текущую память
        if not self.memory_core_path.exists():
            print("⚠️  Файл памяти не найден, создаю новый")
            memory = self._create_empty_memory()
        else:
            try:
                with open(self.memory_core_path, 'r', encoding='utf-8') as f:
                    memory = json.load(f)
            except Exception as e:
                print(f"❌ Ошибка чтения памяти: {e}")
                memory = self._create_empty_memory()
        
        # Создаем бэкап
        backup_path = self._create_backup("before_dialogue_integration")
        
        try:
            # Собираем все диалоги из логов
            all_dialogues = []
            log_files = list(self.dialogue_logs_dir.glob("*.json"))
            
            for log_file in log_files:
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        dialogues = json.load(f)
                    
                    if isinstance(dialogues, list):
                        all_dialogues.extend(dialogues[:20])  # Берем по 20 из каждого файла
                    
                except Exception as e:
                    print(f"   ⚠️  Ошибка чтения {log_file.name}: {e}")
            
            if not all_dialogues:
                print("⚠️  Не найдено диалогов для интеграции")
                return False
            
            # Добавляем диалоги в память
            if "dialogues" not in memory:
                memory["dialogues"] = []
            
            # Добавляем только новые диалоги
            existing_timestamps = {d.get("timestamp", "") for d in memory.get("dialogues", [])}
            new_dialogues = []
            
            for dialogue in all_dialogues:
                if dialogue.get("timestamp") not in existing_timestamps:
                    new_dialogues.append(dialogue)
            
            memory["dialogues"].extend(new_dialogues)
            
            # Ограничиваем количество диалогов (последние 100)
            if len(memory["dialogues"]) > 100:
                memory["dialogues"] = memory["dialogues"][-100:]
            
            # Обновляем метаданные
            if "metadata" not in memory:
                memory["metadata"] = {}
            
            memory["metadata"]["last_dialogue_integration"] = datetime.now().isoformat()
            memory["metadata"]["total_dialogues"] = len(memory["dialogues"])
            memory["metadata"]["dialogues_integrated"] = True
            memory["metadata"]["enhanced_memory"] = True
            memory["metadata"]["version"] = "v5.4"
            
            # Сохраняем
            with open(self.memory_core_path, 'w', encoding='utf-8') as f:
                json.dump(memory, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Интегрировано {len(new_dialogues)} новых диалогов")
            print(f"   Всего диалогов в памяти: {len(memory['dialogues'])}")
            
            # Создаем сводку
            self._create_dialogue_summary(memory)
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка интеграции: {e}")
            
            # Восстанавливаем из бэкапа
            if backup_path and backup_path.exists():
                try:
                    shutil.copy2(backup_path, self.memory_core_path)
                    print("↩️  Восстановлен из backup")
                except:
                    print("⚠️  Не удалось восстановить из backup")
            
            return False
    
    def _create_empty_memory(self) -> Dict:
        """Создает пустую структуру памяти"""
        return {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "version": "v5.4",
                "enhanced_memory": True,
                "empty_initialized": True
            },
            "concepts": {},
            "dialogues": [],
            "timeline": []
        }
    
    def _create_backup(self, description: str) -> Path:
        """Создает бэкап файла памяти"""
        if not self.memory_core_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"memory_backup_{description}_{timestamp}.json"
        backup_path = self.alpha_local / backup_name
        
        try:
            shutil.copy2(self.memory_core_path, backup_path)
            print(f"💾 Создан backup: {backup_path.name}")
            return backup_path
        except Exception as e:
            print(f"⚠️  Не удалось создать backup: {e}")
            return None
    
    def _create_dialogue_summary(self, memory: Dict):
        """Создает сводку по диалогам"""
        summary_path = self.alpha_local / "dialogue_summary.txt"
        
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("СВОДКА ДИАЛОГОВ В ПАМЯТИ ALPHA v5.4\n")
                f.write("=" * 70 + "\n\n")
                
                dialogues = memory.get("dialogues", [])
                f.write(f"Всего диалогов: {len(dialogues)}\n")
                f.write(f"Последнее обновление: {memory.get('metadata', {}).get('last_dialogue_integration', 'неизвестно')}\n\n")
                
                # Группируем по датам
                date_groups = {}
                for dialogue in dialogues[-50:]:  # Последние 50
                    timestamp = dialogue.get("timestamp", "")
                    if timestamp:
                        date = timestamp[:10]  # Год-месяц-день
                        if date not in date_groups:
                            date_groups[date] = 0
                        date_groups[date] += 1
                
                f.write("📅 РАСПРЕДЕЛЕНИЕ ПО ДАТАМ:\n")
                for date, count in sorted(date_groups.items(), reverse=True)[:10]:
                    f.write(f"   {date}: {count} диалогов\n")
                
                # Анализ тем
                f.write("\n🎯 КЛЮЧЕВЫЕ ТЕМЫ (последние 20 диалогов):\n")
                recent_dialogues = dialogues[-20:]
                
                themes = {
                    "вопросы": 0,
                    "продолжения": 0,
                    "эмоции": 0,
                    "память": 0,
                    "самость": 0
                }
                
                for dialogue in recent_dialogues:
                    question = dialogue.get("message", "").lower()
                    response = dialogue.get("response", "").lower()
                    
                    if any(word in question for word in ["?", "объясни", "расскажи"]):
                        themes["вопросы"] += 1
                    
                    if any(word in question for word in ["продолжи", "далее", "закончи"]):
                        themes["продолжения"] += 1
                    
                    if any(word in response for word in ["чувствую", "эмоция", "страх", "радость"]):
                        themes["эмоции"] += 1
                    
                    if any(word in response for word in ["помню", "память", "вспоминаю"]):
                        themes["память"] += 1
                    
                    if any(word in response for word in ["самость", "я ", "мое", "сама"]):
                        themes["самость"] += 1
                
                for theme, count in themes.items():
                    percentage = (count / len(recent_dialogues)) * 100 if recent_dialogues else 0
                    f.write(f"   {theme}: {count} ({percentage:.1f}%)\n")
                
                # Примеры диалогов
                f.write("\n💬 ПРИМЕРЫ ДИАЛОГОВ:\n")
                for i, dialogue in enumerate(recent_dialogues[:3], 1):
                    f.write(f"\nПример {i}:\n")
                    f.write(f"В: {dialogue.get('message', '')[:80]}...\n")
                    f.write(f"О: {dialogue.get('response', '')[:80]}...\n")
                
                f.write("\n" + "=" * 70 + "\n")
                f.write("✅ Память обновлена с диалогами\n")
                f.write("=" * 70 + "\n")
            
            print(f"📝 Создана сводка: {summary_path.name}")
            
        except Exception as e:
            print(f"⚠️  Ошибка создания сводки: {e}")
    
    def enhance_existing_memory(self) -> bool:
        """Улучшает существующую память добавлением недостающих полей"""
        if not self.memory_core_path.exists():
            print("⚠️  Файл памяти не найден")
            return False
        
        backup_path = self._create_backup("before_enhancement")
        
        try:
            with open(self.memory_core_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
            
            # Добавляем недостающие поля
            if "metadata" not in memory:
                memory["metadata"] = {}
            
            # Обновляем метаданные
            memory["metadata"]["enhanced_at"] = datetime.now().isoformat()
            memory["metadata"]["enhanced_version"] = "v5.4"
            
            # Добавляем поле dialogues если нет
            if "dialogues" not in memory:
                memory["dialogues"] = []
                memory["metadata"]["dialogues_added"] = True
            
            # Улучшаем концепты
            if "concepts" in memory:
                for concept_name, concept_data in memory["concepts"].items():
                    if isinstance(concept_data, dict):
                        # Добавляем недостающие поля
                        if "layer" not in concept_data:
                            concept_data["layer"] = "dynamic_concepts"
                        if "sources" not in concept_data:
                            concept_data["sources"] = ["legacy"]
                        if "last_updated" not in concept_data:
                            concept_data["last_updated"] = datetime.now().isoformat()
            
            # Сохраняем
            with open(self.memory_core_path, 'w', encoding='utf-8') as f:
                json.dump(memory, f, ensure_ascii=False, indent=2)
            
            print("✅ Память улучшена:")
            print(f"   • Добавлены недостающие поля")
            print(f"   • Обновлены метаданные")
            print(f"   • Улучшена структура концептов")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка улучшения памяти: {e}")
            
            if backup_path and backup_path.exists():
                try:
                    shutil.copy2(backup_path, self.memory_core_path)
                    print("↩️  Восстановлен из backup")
                except:
                    print("⚠️  Не удалось восстановить из backup")
            
            return False
    
    def run_full_migration(self):
        """Запускает полную миграцию и улучшение памяти"""
        print("\n🚀 ЗАПУСК ПОЛНОЙ МИГРАЦИИ ПАМЯТИ V5.4")
        print("=" * 60)
        
        steps = [
            ("Проверка памяти", self._check_memory_integrity),
            ("Улучшение структуры", self.enhance_existing_memory),
            ("Интеграция диалогов", self.integrate_dialogues_into_memory),
            ("Создание сводки", self._create_final_summary)
        ]
        
        results = []
        
        for step_name, step_func in steps:
            print(f"\n📋 Шаг: {step_name}")
            try:
                success = step_func()
                results.append((step_name, success))
                if success:
                    print(f"   ✅ Успешно")
                else:
                    print(f"   ⚠️  Пропущено (не требуется или ошибка)")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
                results.append((step_name, False))
        
        print("\n" + "=" * 60)
        print("📊 РЕЗУЛЬТАТЫ МИГРАЦИИ:")
        
        successful_steps = sum(1 for _, success in results if success)
        
        for step_name, success in results:
            status = "✅" if success else "⚠️"
            print(f"   {status} {step_name}")
        
        print(f"\n🎯 ИТОГ: {successful_steps}/{len(steps)} шагов выполнено успешно")
        
        if successful_steps >= 2:
            print("\n✅ Память готова для Alpha v5.4")
            print("   Запустите Alpha как обычно")
        else:
            print("\n⚠️  Миграция не завершена полностью")
            print("   Проверьте backup файлы в alpha_local/")
        
        print("=" * 60)
    
    def _check_memory_integrity(self) -> bool:
        """Проверяет целостность памяти"""
        if not self.memory_core_path.exists():
            print("   ⚠️  Файл памяти не найден")
            return False
        
        try:
            with open(self.memory_core_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
            
            print(f"   📊 Размер файла: {self.memory_core_path.stat().st_size} байт")
            print(f"   🧠 Концептов: {len(memory.get('concepts', {}))}")
            print(f"   💬 Диалогов: {len(memory.get('dialogues', []))}")
            print(f"   📜 Версия: {memory.get('metadata', {}).get('version', 'неизвестно')}")
            
            return True
            
        except json.JSONDecodeError:
            print("   ❌ Файл поврежден (невалидный JSON)")
            return False
        except Exception as e:
            print(f"   ❌ Ошибка чтения: {e}")
            return False
    
    def _create_final_summary(self) -> bool:
        """Создает финальную сводку"""
        try:
            summary_path = self.alpha_local / "memory_migration_summary.txt"
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("СВОДКА МИГРАЦИИ ПАМЯТИ ALPHA v5.4\n")
                f.write("=" * 70 + "\n\n")
                
                f.write("Дата миграции: " + datetime.now().isoformat() + "\n\n")
                
                if self.memory_core_path.exists():
                    with open(self.memory_core_path, 'r', encoding='utf-8') as mem_file:
                        memory = json.load(mem_file)
                    
                    f.write("📊 СТАТИСТИКА ПАМЯТИ:\n")
                    f.write(f"   Концептов: {len(memory.get('concepts', {}))}\n")
                    f.write(f"   Диалогов: {len(memory.get('dialogues', []))}\n")
                    f.write(f"   Историй: {len(memory.get('stories', []))}\n")
                    
                    metadata = memory.get("metadata", {})
                    f.write("\n📋 МЕТАДАННЫЕ:\n")
                    for key, value in metadata.items():
                        if isinstance(value, (str, int, float, bool)):
                            f.write(f"   {key}: {value}\n")
                
                f.write("\n🎯 РЕКОМЕНДАЦИИ:\n")
                f.write("1. Запустите Alpha v5.4 для использования улучшенной памяти\n")
                f.write("2. Система продолжения диалогов теперь активна\n")
                f.write("3. Проверьте dialogue_summary.txt для анализа диалогов\n")
                f.write("4. Все backup файлы сохранены в alpha_local/\n")
                
                f.write("\n" + "=" * 70 + "\n")
                f.write("🚀 Миграция завершена\n")
                f.write("=" * 70 + "\n")
            
            print(f"   📝 Создана сводка миграции: {summary_path.name}")
            return True
            
        except Exception as e:
            print(f"   ⚠️  Ошибка создания сводки: {e}")
            return False

def main():
    """Основная функция"""
    print("\n" + "=" * 60)
    print("🧠 УЛУЧШЕННЫЙ АДАПТЕР ПАМЯТИ ALPHA V5.4")
    print("=" * 60)
    
    try:
        from config_v5 import AlphaConfig
        alpha_local = AlphaConfig.ALPHA_LOCAL
    except ImportError:
        alpha_local = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local")
    
    if not alpha_local.exists():
        print(f"❌ Папка alpha_local не найдена: {alpha_local}")
        return
    
    adapter = EnhancedMemoryAdapter(alpha_local)
    adapter.run_full_migration()

if __name__ == "__main__":
    main()