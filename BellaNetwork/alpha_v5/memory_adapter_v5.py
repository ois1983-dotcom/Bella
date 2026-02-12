# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\memory_adapter_v5.py
"""
АДАПТЕР ПАМЯТИ V5.2 - УЛУЧШЕННАЯ ВЕРСИЯ ДЛЯ ВСЕХ ФОРМАТОВ
Распознает все версии памяти от v4.3 до v5.1
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import shutil

class MemoryAdapterV5:
    """
    УЛУЧШЕННЫЙ адаптер, который распознает ВСЕ форматы памяти
    """
    
    def __init__(self, alpha_local_path: Path):
        self.alpha_local = Path(alpha_local_path)
        self.memory_core_path = self.alpha_local / "alpha_memory_core.json"
        
        print("=" * 60)
        print("🧠 УЛУЧШЕННЫЙ АДАПТЕР ПАМЯТИ V5.2")
        print("=" * 60)
    
    def detect_memory_format(self, memory: Dict) -> str:
        """Определяет формат памяти по ее структуре"""
        
        # Проверяем наличие ключевых полей
        has_metadata = "metadata" in memory
        has_concepts = "concepts" in memory
        
        if not has_metadata or not has_concepts:
            return "invalid"
        
        metadata = memory["metadata"]
        
        # Определяем по версии
        version = metadata.get("alpha_version", metadata.get("version", "unknown"))
        
        if version in ["v5.1", "v5.2", "5.1", "5.2"]:
            return "modern"
        elif version in ["v4.3", "4.3"]:
            return "v4_3_legacy"
        elif "network_version" in metadata and "BellaNetwork" in str(metadata.get("network_version", "")):
            return "v4_3_legacy"
        elif "total_mentions" in metadata and "total_concepts" in metadata:
            return "v4_3_legacy"
        elif "created_at" in metadata and isinstance(metadata["created_at"], str):
            # Проверяем структуру concepts
            concepts = memory.get("concepts", {})
            if concepts:
                first_concept = next(iter(concepts.values()))
                if isinstance(first_concept, dict) and "total_mentions" in first_concept:
                    return "v4_3_legacy"
        
        return "unknown"
    
    def check_current_memory(self) -> Dict:
        """Проверяет текущую структуру памяти"""
        if not self.memory_core_path.exists():
            return {
                "exists": False,
                "message": "Файл памяти не найден. Alpha создаст новый автоматически.",
                "safe_to_proceed": True
            }
        
        try:
            with open(self.memory_core_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
            
            # Определяем формат
            memory_format = self.detect_memory_format(memory)
            
            # Анализируем структуру
            analysis = {
                "exists": True,
                "file_size": self.memory_core_path.stat().st_size,
                "format": memory_format,
                "has_metadata": "metadata" in memory,
                "has_concepts": "concepts" in memory,
                "concepts_count": len(memory.get("concepts", {})),
                "memory_structure": list(memory.keys())
            }
            
            # Добавляем версию если есть
            if "metadata" in memory:
                metadata = memory["metadata"]
                analysis["version"] = metadata.get("alpha_version", metadata.get("version", "unknown"))
                analysis["created_at"] = metadata.get("created_at", "unknown")
            
            # Определяем безопасность
            if memory_format == "modern":
                analysis["message"] = "Память уже в современном формате v5.x"
                analysis["safe_to_proceed"] = True
            elif memory_format == "v4_3_legacy":
                analysis["message"] = "Память в формате v4.3 (от memory_miner.py)"
                analysis["safe_to_proceed"] = False
            elif memory_format == "invalid":
                analysis["message"] = "Память повреждена или имеет неверный формат"
                analysis["safe_to_proceed"] = False
            else:
                analysis["message"] = "Неизвестный формат памяти"
                analysis["safe_to_proceed"] = False
            
            return analysis
            
        except json.JSONDecodeError as e:
            return {
                "exists": True,
                "error": f"JSON ошибка: {e}",
                "message": "Файл памяти поврежден (невалидный JSON)",
                "safe_to_proceed": False
            }
        except Exception as e:
            return {
                "exists": True,
                "error": str(e),
                "message": "Ошибка чтения файла памяти",
                "safe_to_proceed": False
            }
    
    def create_safe_backup(self, description: str = "") -> Optional[Path]:
        """Создает безопасную резервную копию"""
        if not self.memory_core_path.exists():
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desc = f"_{description}" if description else ""
            backup_name = f"alpha_memory_backup{desc}_{timestamp}.json"
            backup_path = self.alpha_local / backup_name
            
            shutil.copy2(self.memory_core_path, backup_path)
            
            print(f"✅ Создан backup: {backup_path.name}")
            return backup_path
            
        except Exception as e:
            print(f"❌ Ошибка создания backup: {e}")
            return None
    
    def convert_v43_to_v52(self, backup_first: bool = True) -> bool:
        """
        Безопасно конвертирует память из формата v4.3 в v5.2
        Сохраняет все данные
        """
        # 1. Проверяем текущую память
        analysis = self.check_current_memory()
        
        if not analysis["exists"]:
            print("✅ Память не найдена, будет создана новая")
            return True
        
        if analysis["format"] != "v4_3_legacy":
            print(f"ℹ️  Память уже в правильном формате: {analysis['format']}")
            return True
        
        print(f"🔄 Обнаружена память старого формата: {analysis['message']}")
        print(f"   Концептов: {analysis['concepts_count']}")
        print(f"   Версия: {analysis.get('version', 'неизвестно')}")
        
        # 2. Создаем backup
        if backup_first:
            backup = self.create_safe_backup("before_v52_conversion")
            if not backup:
                print("❌ Не удалось создать backup, отмена конвертации")
                return False
        
        try:
            # 3. Загружаем старую память
            with open(self.memory_core_path, 'r', encoding='utf-8') as f:
                old_memory = json.load(f)
            
            # 4. Создаем новую структуру v5.2
            new_memory = {
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "original_created_at": old_memory.get("metadata", {}).get("created_at", datetime.now().isoformat()),
                    "alpha_version": "v5.2",
                    "converted_from": "v4_3_legacy",
                    "conversion_date": datetime.now().isoformat(),
                    "original_concepts_count": analysis["concepts_count"],
                    "original_version": analysis.get("version", "unknown"),
                    "source": "memory_adapter_v5_improved_conversion"
                },
                "concepts": {},
                "dialogue_stats": {
                    "total_interactions": 0,
                    "first_interaction": datetime.now().isoformat(),
                    "last_interaction": datetime.now().isoformat()
                }
            }
            
            # 5. Конвертируем концепты
            concepts_converted = 0
            old_concepts = old_memory.get("concepts", {})
            
            for concept_name, concept_data in old_concepts.items():
                try:
                    if isinstance(concept_data, dict):
                        # Старый формат: {"total_mentions": X, "contexts": [], "sources": []}
                        mentions = concept_data.get("total_mentions", 0)
                        contexts = concept_data.get("contexts", [])
                        sources = concept_data.get("sources", [])
                        
                        # Конвертируем sources если это set
                        if isinstance(sources, set):
                            sources = list(sources)
                        
                        new_concept = {
                            "total_mentions": mentions,
                            "first_seen": datetime.now().isoformat(),
                            "last_updated": datetime.now().isoformat(),
                            "original_source": "v4_3_memory_miner",
                            "converted": True,
                            "converted_at": datetime.now().isoformat(),
                            "legacy_data_preserved": len(contexts) > 0
                        }
                        
                        # Сохраняем источники если есть
                        if sources:
                            new_concept["sources"] = sources
                        else:
                            new_concept["sources"] = ["legacy_conversion"]
                        
                        new_memory["concepts"][concept_name] = new_concept
                        concepts_converted += 1
                        
                    elif isinstance(concept_data, (int, float)):
                        # Просто число
                        new_memory["concepts"][concept_name] = {
                            "total_mentions": int(concept_data),
                            "first_seen": datetime.now().isoformat(),
                            "last_updated": datetime.now().isoformat(),
                            "original_source": "v4_3_memory_miner_numeric",
                            "converted": True,
                            "converted_at": datetime.now().isoformat(),
                            "sources": ["legacy_conversion"]
                        }
                        concepts_converted += 1
                        
                except Exception as e:
                    print(f"   ⚠️  Ошибка конвертации концепта '{concept_name}': {e}")
            
            # 6. Сохраняем дополнительную информацию из старой памяти
            if "timeline" in old_memory:
                new_memory["legacy_timeline_preserved"] = True
                new_memory["legacy_timeline_entries"] = len(old_memory["timeline"])
            
            if "stories" in old_memory:
                new_memory["legacy_stories_preserved"] = True
                new_memory["legacy_stories_count"] = len(old_memory["stories"])
            
            # 7. Сохраняем новую память
            with open(self.memory_core_path, 'w', encoding='utf-8') as f:
                json.dump(new_memory, f, ensure_ascii=False, indent=2)
            
            # 8. Сохраняем старую память как архив
            archive_path = self.alpha_local / f"alpha_memory_v43_archived_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(archive_path, 'w', encoding='utf-8') as f:
                json.dump(old_memory, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ КОНВЕРТАЦИЯ ЗАВЕРШЕНА:")
            print(f"   Концептов сконвертировано: {concepts_converted}/{analysis['concepts_count']}")
            print(f"   Новый формат: v5.2")
            print(f"   📁 Архив старой памяти: {archive_path.name}")
            print(f"   💾 Backup создан: {backup.name if backup_first else 'нет'}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Ошибка конвертации: {e}")
            
            # Пытаемся восстановить из backup
            if backup_first and 'backup' in locals() and backup:
                try:
                    shutil.copy2(backup, self.memory_core_path)
                    print("↩️  Восстановлен из backup")
                except Exception as restore_error:
                    print(f"⚠️  Не удалось восстановить из backup: {restore_error}")
            
            return False
    
    def repair_memory_file(self) -> bool:
        """Пытается восстановить поврежденный файл памяти"""
        if not self.memory_core_path.exists():
            print("❌ Файл памяти не найден для восстановления")
            return False
        
        # Создаем backup перед восстановлением
        backup = self.create_safe_backup("before_repair")
        if not backup:
            print("⚠️  Не удалось создать backup перед восстановлением")
        
        try:
            # Читаем файл как текст
            with open(self.memory_core_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Пытаемся найти JSON в файле
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_content = content[json_start:json_end]
                memory = json.loads(json_content)
                
                # Сохраняем восстановленный файл
                with open(self.memory_core_path, 'w', encoding='utf-8') as f:
                    json.dump(memory, f, ensure_ascii=False, indent=2)
                
                print("✅ Файл памяти восстановлен")
                return True
            else:
                print("❌ Не удалось найти JSON в файле")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка восстановления: {e}")
            return False
    
    def run_safe_migration(self, force_conversion: bool = False):
        """
        ПОЛНАЯ БЕЗОПАСНАЯ МИГРАЦИЯ ДЛЯ НОВИЧКОВ
        """
        print("\n" + "=" * 60)
        print("🚀 ЗАПУСК УЛУЧШЕННОЙ МИГРАЦИИ ДЛЯ НОВИЧКА")
        print("=" * 60)
        
        # Шаг 1: Анализ
        print("\n📊 ШАГ 1: АНАЛИЗ ТЕКУЩЕЙ ПАМЯТИ")
        analysis = self.check_current_memory()
        
        print("   Обнаружено:")
        for key, value in analysis.items():
            if key not in ["safe_to_proceed", "memory_structure"] and not key.startswith("_"):
                print(f"   • {key}: {value}")
        
        # Шаг 2: Решение
        print("\n🎯 ШАГ 2: РЕКОМЕНДАЦИЯ")
        
        if not analysis["exists"]:
            print("   ✅ Память не найдена, Alpha создаст новую автоматически")
            print("   Действие: запустите Alpha v5.2 как обычно")
            return True
        
        if analysis["format"] == "invalid":
            print("   ❌ Память повреждена")
            print("   Действие: попытаться восстановить или создать новую")
            
            response = input("\n   Попытаться восстановить память? (y/n): ").strip().lower()
            if response == 'y':
                if self.repair_memory_file():
                    print("   ✅ Восстановление успешно, запустите адаптер снова")
                else:
                    print("   ❌ Восстановление не удалось, будет создана новая память")
            return False
        
        if analysis["safe_to_proceed"] and not force_conversion:
            print("   ✅ Память уже совместима с v5.2")
            print("   Действие: запустите Alpha v5.2 как обычно")
            return True
        
        # Шаг 3: Конвертация
        print("\n🔄 ШАГ 3: КОНВЕРТАЦИЯ")
        
        if analysis["format"] == "v4_3_legacy" or force_conversion:
            print(f"   Обнаружена память от memory_miner.py v4.3")
            print(f"   Концептов для конвертации: {analysis['concepts_count']}")
            print(f"   Размер файла: {analysis['file_size']} байт")
            
            print("\n   ⚠️  ВНИМАНИЕ: перед конвертацией будет создан backup")
            print("   Все данные сохранятся в архиве")
            
            response = input("\n   Продолжить конвертацию? (y/n): ").strip().lower()
            if response == 'y':
                print("\n   Начинаю безопасную конвертацию...")
                success = self.convert_v43_to_v52(backup_first=True)
                
                if success:
                    print("\n   ✅ КОНВЕРТАЦИЯ УСПЕШНА!")
                    print("   Теперь можно запускать Alpha v5.2")
                    return True
                else:
                    print("\n   ❌ Конвертация не удалась")
                    print("   Проверьте backup файлы в папке alpha_local/")
                    return False
            else:
                print("\n   ⚠️  Конвертация отменена")
                print("   Alpha v5.2 может работать некорректно со старой памятью")
                return False
        
        print("\n   ⚠️  Неизвестная ситуация")
        print("   Рекомендуется создать backup вручную")
        return False
    
    def show_memory_info(self):
        """Показывает детальную информацию о памяти"""
        if not self.memory_core_path.exists():
            print("Файл памяти не найден")
            return
        
        try:
            with open(self.memory_core_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
            
            print("\n" + "=" * 60)
            print("ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О ПАМЯТИ")
            print("=" * 60)
            
            # Метаданные
            if "metadata" in memory:
                print("\n📋 МЕТАДАННЫЕ:")
                metadata = memory["metadata"]
                for key, value in metadata.items():
                    if isinstance(value, (str, int, float, bool)):
                        print(f"   {key}: {value}")
            
            # Концепты
            if "concepts" in memory:
                concepts = memory["concepts"]
                print(f"\n🧠 КОНЦЕПТЫ: {len(concepts)}")
                
                # Топ-10 по упоминаниям
                sorted_concepts = sorted(concepts.items(), 
                                       key=lambda x: x[1].get("total_mentions", 0), 
                                       reverse=True)
                
                print("   Топ-10 концептов:")
                for i, (name, data) in enumerate(sorted_concepts[:10], 1):
                    mentions = data.get("total_mentions", 0)
                    print(f"   {i}. {name}: {mentions} упоминаний")
            
            # Диалоговая статистика
            if "dialogue_stats" in memory:
                print("\n💬 ДИАЛОГОВАЯ СТАТИСТИКА:")
                stats = memory["dialogue_stats"]
                for key, value in stats.items():
                    print(f"   {key}: {value}")
            
            # Legacy данные
            legacy_fields = ["stories", "timeline", "concept_relationships"]
            for field in legacy_fields:
                if field in memory:
                    count = len(memory[field]) if isinstance(memory[field], (list, dict)) else 1
                    print(f"\n📜 {field.upper()}: {count} записей сохранено")
            
            print("\n" + "=" * 60)
            
        except Exception as e:
            print(f"Ошибка чтения памяти: {e}")

def main():
    """Основная функция для новичков"""
    print("\n" + "=" * 60)
    print("🧠 УЛУЧШЕННЫЙ АДАПТЕР ПАМЯТИ ALPHA V5.2")
    print("=" * 60)
    print("Эта программа безопасно подготовит память для Alpha v5.2")
    print("Она распознает ВСЕ форматы памяти от v4.3 до v5.1")
    print("=" * 60)
    
    import sys
    
    # Проверяем аргументы командной строки
    force = "--force" in sys.argv
    info = "--info" in sys.argv
    
    # Импортируем конфиг
    try:
        from config_v5 import AlphaConfig
        alpha_local = AlphaConfig.ALPHA_LOCAL
    except ImportError:
        # Если нет конфига, используем стандартный путь
        alpha_local = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local")
    
    if not alpha_local.exists():
        print(f"❌ Папка alpha_local не найдена: {alpha_local}")
        print("Создайте папку alpha_local вручную или запустите Alpha для автоматического создания")
        return
    
    adapter = MemoryAdapterV5(alpha_local)
    
    if info:
        # Показать информацию о памяти
        adapter.show_memory_info()
        return
    
    # Показать текущее состояние
    print("\n📁 Проверяю текущую память...")
    
    # Запускаем безопасную миграцию
    success = adapter.run_safe_migration(force_conversion=force)
    
    print("\n" + "=" * 60)
    if success:
        print("✅ МИГРАЦИЯ ЗАВЕРШЕНА УСПЕШНО")
        print("Теперь можно запускать Alpha v5.2:")
        print("   python run_alpha_v5.py")
    else:
        print("⚠️  МИГРАЦИЯ НЕ ЗАВЕРШЕНА")
        print("Проверьте backup файлы в папке alpha_local/")
        print("При необходимости запустите адаптер снова")
    
    print("\n💡 СОВЕТЫ:")
    print("1. Для просмотра информации о памяти: python memory_adapter_v5.py --info")
    print("2. Для принудительной конвертации: python memory_adapter_v5.py --force")
    print("3. Все backup файлы находятся в папке alpha_local/")
    print("=" * 60)

if __name__ == "__main__":
    main()