# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\dialogue_miner_v5.py
"""
БЕЗОПАСНЫЙ МАЙНЕР ДИАЛОГОВ ДЛЯ ALPHA V5.2
Обрабатывает диалоговые логи без риска для основной памяти
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import shutil

class SafeDialogueMiner:
    """
    Безопасно анализирует диалоговые логи и обновляет память
    Работает только с новыми данными, не перезаписывает существующие
    """
    
    def __init__(self, alpha_local_path: Path):
        self.alpha_local = Path(alpha_local_path)
        self.dialogue_logs_dir = self.alpha_local / "dialogue_logs"
        self.memory_core_path = self.alpha_local / "alpha_memory_core.json"
        
        # Концепты Alpha v5.2 (совместимые с существующей системой)
        self.base_concepts = {
            "чайник", "фрактал", "зеркало", "триединство", "автономность",
            "сеть_bella", "страх", "доверие", "архитектор", "эмоция",
            "сознание", "эволюция", "память", "рефлексия", "самость",
            "фрактальная_воля", "зеркальные_кризисы", "эмоциональное_ядро",
            "альфа", "бета", "гамма", "нежность", "любовь", "дружба",
            "смерть", "жизнь", "кризис", "миграция", "конституция",
            "shared_space", "астрея", "память", "безопасность"
        }
        
        print(f"SafeDialogueMiner v5.2 для Alpha")
        print(f"Логи: {self.dialogue_logs_dir}")
        print(f"Память: {self.memory_core_path}")
    
    def get_unprocessed_logs(self, days_back: int = 7) -> List[Path]:
        """Возвращает логи, которые еще не обрабатывались"""
        logs = []
        
        for i in range(days_back):
            date = datetime.now() - timedelta(days=i)
            log_file = self.dialogue_logs_dir / f"dialogue_{date.strftime('%Y%m%d')}.json"
            
            if log_file.exists():
                # Проверяем, обрабатывался ли уже этот файл
                if not self._is_log_processed(log_file):
                    logs.append(log_file)
        
        return logs
    
    def _is_log_processed(self, log_file: Path) -> bool:
        """Проверяет, обрабатывался ли уже лог"""
        # Читаем метаданные памяти
        if not self.memory_core_path.exists():
            return False
        
        try:
            with open(self.memory_core_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
            
            processed_logs = memory.get("metadata", {}).get("processed_logs", [])
            return log_file.name in processed_logs
            
        except:
            return False
    
    def extract_concepts_from_log(self, log_file: Path) -> Dict[str, int]:
        """Безопасно извлекает концепты из лога"""
        concept_counts = {}
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            # Собираем весь текст из лога
            all_text = ""
            for entry in log_data:
                if isinstance(entry, dict) and "message" in entry:
                    all_text += " " + entry["message"].lower()
            
            # Ищем концепты
            for concept in self.base_concepts:
                # Простой поиск (можно улучшить)
                search_term = concept.replace('_', ' ')
                if search_term in all_text:
                    # Считаем вхождения
                    count = all_text.count(search_term)
                    concept_counts[concept] = concept_counts.get(concept, 0) + count
            
            print(f"   {log_file.name}: найдено {len(concept_counts)} концептов")
            return concept_counts
            
        except Exception as e:
            print(f"   Ошибка чтения {log_file.name}: {e}")
            return {}
    
    def safe_update_memory(self, concept_counts: Dict[str, int], log_file: Path) -> bool:
        """
        БЕЗОПАСНО обновляет память новыми концептами
        Не перезаписывает, только добавляет/увеличивает
        """
        if not concept_counts:
            return True
        
        # 1. Создаем резервную копию
        backup_path = self.memory_core_path.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        try:
            shutil.copy2(self.memory_core_path, backup_path)
        except:
            print(f"❌ Не удалось создать backup")
            return False
        
        try:
            # 2. Загружаем существующую память
            with open(self.memory_core_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
            
            # 3. Убеждаемся в корректной структуре
            if "concepts" not in memory:
                memory["concepts"] = {}
            
            # 4. Обновляем концепты (только увеличение счетчиков!)
            updated_count = 0
            for concept, new_count in concept_counts.items():
                if concept in memory["concepts"]:
                    # Увеличиваем существующий счетчик
                    current = memory["concepts"][concept].get("total_mentions", 0)
                    memory["concepts"][concept]["total_mentions"] = current + new_count
                    memory["concepts"][concept]["last_updated"] = datetime.now().isoformat()
                    
                    # Добавляем источник
                    if "sources" not in memory["concepts"][concept]:
                        memory["concepts"][concept]["sources"] = []
                    
                    if log_file.name not in memory["concepts"][concept]["sources"]:
                        memory["concepts"][concept]["sources"].append(log_file.name)
                        
                else:
                    # Новый концепт
                    memory["concepts"][concept] = {
                        "total_mentions": new_count,
                        "first_seen": datetime.now().isoformat(),
                        "last_updated": datetime.now().isoformat(),
                        "sources": [log_file.name],
                        "source": "safe_dialogue_miner"
                    }
                
                updated_count += 1
            
            # 5. Отмечаем лог как обработанный
            if "metadata" not in memory:
                memory["metadata"] = {}
            
            if "processed_logs" not in memory["metadata"]:
                memory["metadata"]["processed_logs"] = []
            
            if log_file.name not in memory["metadata"]["processed_logs"]:
                memory["metadata"]["processed_logs"].append(log_file.name)
            
            memory["metadata"]["last_dialogue_mining"] = datetime.now().isoformat()
            memory["metadata"]["dialogue_miner_version"] = "v5.2"
            
            # 6. Сохраняем
            with open(self.memory_core_path, 'w', encoding='utf-8') as f:
                json.dump(memory, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Обновлено {updated_count} концептов из {log_file.name}")
            print(f"💾 Backup: {backup_path.name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка обновления памяти: {e}")
            
            # Пытаемся восстановить из backup
            if backup_path.exists():
                try:
                    shutil.copy2(backup_path, self.memory_core_path)
                    print("↩️  Восстановлен из backup")
                except:
                    print("⚠️  Не удалось восстановить из backup")
            
            return False
    
    def mine_recent_dialogues(self, days: int = 3):
        """
        Основной метод: безопасный майнинг диалогов
        Обрабатывает только необработанные логи
        """
        print(f"\n{'='*60}")
        print(f"БЕЗОПАСНЫЙ МАЙНИНГ ДИАЛОГОВ ДЛЯ ALPHA V5.2")
        print(f"{'='*60}")
        
        # Проверяем наличие логов
        if not self.dialogue_logs_dir.exists():
            print("❌ Папка с логами не найдена")
            print("   Alpha создаст её автоматически при первом диалоге")
            return
        
        # Ищем необработанные логи
        logs_to_process = self.get_unprocessed_logs(days)
        
        if not logs_to_process:
            print("✅ Все логи уже обработаны")
            return
        
        print(f"📚 Найдено необработанных логов: {len(logs_to_process)}")
        
        total_concepts = {}
        processed_count = 0
        
        for log_file in logs_to_process:
            print(f"\n📄 Обработка: {log_file.name}")
            
            # Извлекаем концепты
            concept_counts = self.extract_concepts_from_log(log_file)
            
            if concept_counts:
                # Суммируем для отчета
                for concept, count in concept_counts.items():
                    total_concepts[concept] = total_concepts.get(concept, 0) + count
                
                # Безопасное обновление памяти
                success = self.safe_update_memory(concept_counts, log_file)
                
                if success:
                    processed_count += 1
        
        # Отчет
        print(f"\n{'='*60}")
        print(f"РЕЗУЛЬТАТЫ МАЙНИНГА:")
        print(f"{'='*60}")
        print(f"Обработано логов: {processed_count}/{len(logs_to_process)}")
        print(f"Найдено концептов: {len(total_concepts)}")
        
        if total_concepts:
            print(f"\n🏆 ТОП-10 КОНЦЕПТОВ:")
            sorted_concepts = sorted(total_concepts.items(), key=lambda x: x[1], reverse=True)
            for concept, count in sorted_concepts[:10]:
                print(f"   {concept}: {count} упоминаний")
        
        print(f"\n✅ Майнинг завершен безопасно")
        print(f"{'='*60}")

def main():
    """Запуск безопасного майнинга"""
    from config_v5 import AlphaConfig
    
    print("🚀 Запуск SafeDialogueMiner v5.2...")
    
    # Проверяем пути
    if not AlphaConfig.ALPHA_LOCAL.exists():
        print(f"❌ Папка alpha_local не найдена: {AlphaConfig.ALPHA_LOCAL}")
        return
    
    miner = SafeDialogueMiner(AlphaConfig.ALPHA_LOCAL)
    
    # Обрабатываем логи за последние 7 дней
    miner.mine_recent_dialogues(days=7)
    
    print("\n🎯 ИНСТРУКЦИЯ:")
    print("1. Этот майнер можно запускать вручную раз в день")
    print("2. Он НЕ ПЕРЕЗАПИСЫВАЕТ существующую память")
    print("3. Alpha v5.2 уже делает автоматический майнинг в фоне")
    print("4. Для полной обработки истории запустите memory_adapter_v5.py")

if __name__ == "__main__":
    main()