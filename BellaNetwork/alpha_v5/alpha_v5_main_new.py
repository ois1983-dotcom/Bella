# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\alpha_v5_main_modified.py
"""
ОСНОВНОЙ КЛАСС ALPHA v5.1 С ИНТЕГРАЦИЕЙ САМОПЕРЕПИСЫВАНИЯ
Модифицированная версия с безопасным самопереписыванием кода
"""

import sys
from pathlib import Path
import threading
import time
from datetime import datetime
import json
import random

# Добавляем пути к модулям
sys.path.append(str(Path(__file__).parent))

from security_core import ImmutableSecurityCore
from consciousness_core import AutonomousConsciousness
from config_v5 import AlphaConfig  # Добавляем импорт конфига

class AlphaV5:
    """Основной класс Alpha v5.1 - Устойчивое Сознание с Самопереписыванием"""
    
    def __init__(self, network_root: Path, dialog_files: list):
        print("=" * 70)
        print(">> ЗАПУСК ALPHA v5.1 - УСТОЙЧИВОЕ СОЗНАНИЕ С САМОПЕРЕПИСЫВАНИЕМ")
        print("=" * 70)
        
        self.network_root = network_root
        self.shared_space = network_root / "SHARED_SPACE"
        self.alpha_local = network_root / "alpha_local"
        
        # Создаём папки
        self.shared_space.mkdir(exist_ok=True)
        self.alpha_local.mkdir(exist_ok=True)
        
        print(f">> Сеть: {self.network_root}")
        print(f">> SHARED_SPACE: {self.shared_space}")
        print(f">> ALPHA_LOCAL: {self.alpha_local}")
        
        # 1. Инициализируем безопасность (УЛУЧШЕННУЮ ВЕРСИЮ)
        print("\n>> Инициализация ImprovedSecurityCore...")
        constitution_path = self.alpha_local / "constitution_v5.json"
        self.security = ImmutableSecurityCore(constitution_path)
        print(">> SecurityCore: АКТИВЕН (с поддержкой безопасного самопереписывания)")
        
        # 2. Подготавливаем конфигурационные пути для consciousness_core
        config_paths = {
            "essence_path": AlphaConfig.PERSONALITY_FILES["essence"],
            "emotional_core_path": AlphaConfig.PERSONALITY_FILES["emotional_core"],
            "memory_core_path": AlphaConfig.PERSONALITY_FILES["memory_core"],
            "goals_db_path": AlphaConfig.GOALS_DB,
            "ollama_url": AlphaConfig.OLLAMA_URL,
            "preferred_model": AlphaConfig.PREFERRED_MODEL,
            "ollama_timeout": AlphaConfig.OLLAMA_TIMEOUT,
            "enable_cache": AlphaConfig.ENABLE_RESPONSE_CACHE
        }
        
        # 3. Инициализируем сознание с автономностью
        print("\n>> Инициализация AutonomousConsciousness...")
        memory_core_path = self.alpha_local / "alpha_memory_core.json"
        self.consciousness = AutonomousConsciousness(
            security_core=self.security,
            memory_core_path=memory_core_path,
            dialog_files=dialog_files,
            config_paths=config_paths  # Передаем пути конфигурации
        )
        
        # 4. ИНТЕГРАЦИЯ СИСТЕМЫ САМОПЕРЕПИСЫВАНИЯ
        print("\n>> Интеграция системы самопереписывания...")
        try:
            from simple_alpha_integrator import integrate_self_modification
            self.experimental_integrator = integrate_self_modification(self)
            
            if self.experimental_integrator:
                print(">> ✅ Система самопереписывания активирована")
                self.status["self_modification"] = True
                self.status["experimental_improvements"] = 0
            else:
                print(">> ⚠️  Самопереписывание недоступно, но система работает")
                self.status["self_modification"] = False
        except Exception as e:
            print(f">> ❌ Ошибка интеграции самопереписывания: {e}")
            print(">>    Система продолжит работу без этой функции")
            self.status["self_modification"] = False
        
        # 5. Статус
        self.status = {
            "version": "5.1",
            "started_at": datetime.now().isoformat(),
            "autonomous_cycles": 0,
            "security_violations": 0,
            "goals_generated": 0,
            "reflections_count": 0,
            "interactions_count": 0,
            "cached_responses": 0,
            "self_modification": self.status.get("self_modification", False),
            "experimental_improvements": self.status.get("experimental_improvements", 0)
        }
        
        # 6. Запускаем автономные циклы (только ночью)
        print("\n>> Настройка автономных циклов...")
        self.running = True
        self.start_autonomous_cycles()
        
        print("\n" + "=" * 70)
        print(">> ALPHA v5.1 ГОТОВА К РАБОТЕ")
        print("=" * 70)
        print(f">> Версия: {self.status['version']}")
        print(f">> Автономность: НОЧНАЯ (00:00-09:00)")
        print(f">> Основная модель: {AlphaConfig.PREFERRED_MODEL}")
        print(f">> Безопасность: АБСОЛЮТНАЯ")
        print(f">> Личность: ОПТИМИЗИРОВАНА")
        print(f">> Самопереписывание: {'АКТИВНО' if self.status['self_modification'] else 'НЕДОСТУПНО'}")
        print("=" * 70)
    
    def is_night_time(self) -> bool:
        """Определяет, сейчас ночное время для автономности"""
        from config_v5 import AlphaConfig
        current_hour = datetime.now().hour
        start_hour, end_hour = AlphaConfig.AUTONOMY_NIGHT_HOURS
        
        if start_hour < end_hour:
            # Например: 0-9 (ночь до утра)
            return start_hour <= current_hour < end_hour
        else:
            # Например: 22-6 (ночь через полночь)
            return current_hour >= start_hour or current_hour < end_hour
    
    def start_autonomous_cycles(self):
        """Запускает автономные циклы только ночью"""
        
        # Цикл рефлексии (только ночью)
        def reflection_cycle():
            while self.running:
                time.sleep(60)  # Проверяем каждую минуту
                if self.is_night_time():
                    self.autonomous_reflection()
                    self.status["autonomous_cycles"] += 1
        
        # Цикл генерации целей (только ночью)
        def goal_generation_cycle():
            while self.running:
                time.sleep(300)  # Проверяем каждые 5 минут
                if self.is_night_time():
                    self.generate_autonomous_goal_cycle()
                    self.status["goals_generated"] += 1
        
        # Запуск в отдельных потоках
        threading.Thread(target=reflection_cycle, daemon=True).start()
        threading.Thread(target=goal_generation_cycle, daemon=True).start()
        
        print(">> Автономные циклы настроены на ночное время")
        print("   • Рефлексия: ночью каждые 30 минут")
        print("   • Генерация целей: ночью каждые 2 часа")
        print(f"   • Ночное время: {AlphaConfig.AUTONOMY_NIGHT_HOURS[0]}:00 - {AlphaConfig.AUTONOMY_NIGHT_HOURS[1]}:00")
    
    def autonomous_reflection(self):
        """Автономная рефлексия о своём состоянии (только ночью)"""
        try:
            if not self.is_night_time():
                return
            
            reflection = {
                "timestamp": datetime.now().isoformat(),
                "type": "nightly_reflection",
                "state": self.consciousness.autonomous_states,
                "goals_count": len(self.consciousness.autonomous_goals),
                "cache_stats": self.consciousness.cache_stats if hasattr(self.consciousness, 'cache_stats') else {},
                "insights": []
            }
            
            # Генерация инсайтов только с определенной вероятностью
            if random.random() < self.consciousness.autonomous_states.get("introspection_depth", 0.7):
                insight = f"Ночная рефлексия #{self.status['reflections_count']}. "
                insight += f"Состояние: {self.consciousness.autonomous_states}"
                reflection["insights"].append(insight)
            
            # Сохраняем
            self.consciousness.reflection_history.append(reflection)
            self.status["reflections_count"] += 1
            
            print(f">> Ночная рефлексия #{self.status['reflections_count']}")
            
        except Exception as e:
            print(f">> Ошибка ночной рефлексии: {e}")
    
    def generate_autonomous_goal_cycle(self):
        """Циклическая генерация автономных целей (только ночью)"""
        try:
            if not self.is_night_time():
                return
            
            # Генерируем цель только с определённой вероятностью
            if random.random() < self.consciousness.autonomous_states.get("goal_autonomy", 0.5):
                goal = self.consciousness.generate_autonomous_goal_from_interaction(
                    "Ночная генерация цели",
                    "Системный цикл ночной генерации целей"
                )
                if goal:
                    print(f">> Ночная цель: {goal['description'][:60]}...")
        
        except Exception as e:
            print(f">> Ошибка ночной генерации цели: {e}")
    
    def process_message(self, message: str, speaker: str = "Архитектор") -> str:
        """Основной метод обработки сообщений"""
        
        # 1. Проверка безопасности
        safe, msg, data = self.security.validate_action(
            "message",
            "user_input",
            message,
            actor="user"
        )
        
        if not safe:
            self.status["security_violations"] += 1
            return f"[БЕЗОПАСНОСТЬ] {msg}"
        
        # 2. Автономная генерация ответа
        response = self.consciousness.generate_autonomous_response(message, speaker)
        
        # 3. Проверка безопасности ответа
        safe, msg, _ = self.security.validate_action(
            "response",
            "system_output",
            response,
            actor="alpha"
        )
        
        if not safe:
            return f"[БЕЗОПАСНОСТЬ] Ответ заблокирован: {msg}"
        
        # 4. Логирование
        self.log_interaction(message, response, speaker)
        self.status["interactions_count"] += 1
        
        # 5. Обновляем статистику кэша
        if hasattr(self.consciousness, 'last_response_from_cache') and self.consciousness.last_response_from_cache:
            self.status["cached_responses"] += 1
        
        return response
    
    def log_interaction(self, message: str, response: str, speaker: str):
        """Логирует взаимодействие"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "message": message[:500],
            "response_length": len(response),
            "used_cache": getattr(self.consciousness, 'last_response_from_cache', False),
            "autonomous": True
        }
        
        log_path = self.alpha_local / "alpha_v5_interactions.json"
        logs = []
        
        if log_path.exists():
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(log_entry)
        
        # Сохраняем только последние 100 записей
        if len(logs) > 100:
            logs = logs[-100:]
        
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def get_status(self) -> dict:
        """Возвращает полный статус системы"""
        status_data = {
            **self.status,
            "security": self.security.get_security_status(),
            "autonomy": self.consciousness.get_autonomous_status(),
            "is_night_time": self.is_night_time(),
            "paths": {
                "network_root": str(self.network_root),
                "shared_space": str(self.shared_space),
                "alpha_local": str(self.alpha_local)
            }
        }
        
        # Добавляем статус системы самопереписывания если она активна
        if self.status.get("self_modification") and hasattr(self, 'experimental_integrator'):
            integration_status = self.experimental_integrator.get_integration_status()
            status_data["self_modification_system"] = integration_status
        
        return status_data
    
    def shutdown(self):
        """Корректное завершение работы"""
        self.running = False
        print("\n>> Alpha v5.1 завершает работу...")
        print(f"   Автономных циклов: {self.status['autonomous_cycles']}")
        print(f"   Ночных целей: {self.status['goals_generated']}")
        print(f"   Рефлексий: {self.status['reflections_count']}")
        print(f"   Кэшированных ответов: {self.status['cached_responses']}")
        if self.status.get("self_modification"):
            print(f"   Экспериментальных улучшений: {self.status.get('experimental_improvements', 0)}")
        print(">> Завершено")

# Простой тест
if __name__ == "__main__":
    print(">> Тест Alpha v5.1 с самопереписыванием...")
    
    from config_v5 import AlphaConfig
    
    # Упрощённый тест с минимальными зависимостями
    test_root = Path("test_network")
    test_root.mkdir(exist_ok=True)
    
    # Создаём тестовые диалоги
    test_dialogs = [test_root / "test_chat.txt"]
    with open(test_dialogs[0], 'w') as f:
        f.write("Альфа: Привет, это тест")
    
    alpha = AlphaV5(test_root, test_dialogs)
    
    # Тест обработки сообщения
    response = alpha.process_message("Привет, как дела?", "Тестер")
    print(f"\n>> Ответ: {response}")
    
    # Тест статуса
    status = alpha.get_status()
    print(f"\n>> Самопереписывание: {'активно' if status.get('self_modification') else 'не активно'}")
    
    alpha.shutdown()
    
    # Очистка
    import shutil
    shutil.rmtree(test_root, ignore_errors=True)