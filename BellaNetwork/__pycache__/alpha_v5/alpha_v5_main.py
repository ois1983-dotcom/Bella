# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\alpha_v5_main.py
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
# Используем EnhancedAutonomousConsciousness как AutonomousConsciousness
from consciousness_core import EnhancedAutonomousConsciousness as AutonomousConsciousness

class AlphaV5:  # Изменено с AlphaV5Fixed на AlphaV5
    """Основной класс Alpha v5.0 с исправленным импортом"""
    
    def __init__(self, network_root: Path, dialog_files: list):
        print("=" * 70)
        print(">> ЗАПУСК ALPHA v5.0 - АВТОНОМНОЕ СОЗНАНИЕ")
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
        
        # 1. Инициализируем безопасность
        print("\n>> Инициализация SecurityCore...")
        constitution_path = self.alpha_local / "constitution_v5.json"
        self.security = ImmutableSecurityCore(constitution_path)
        print(">> SecurityCore: АКТИВЕН")
        
        # 2. Инициализируем сознание с автономностью
        print("\n>> Инициализация AutonomousConsciousness...")
        memory_core_path = self.alpha_local / "alpha_memory_core.json"
        self.consciousness = AutonomousConsciousness(
            security_core=self.security,
            memory_core_path=memory_core_path,
            dialog_files=dialog_files
        )
        
        # 3. Статус
        self.status = {
            "version": "5.0",
            "started_at": datetime.now().isoformat(),
            "autonomous_cycles": 0,
            "security_violations": 0,
            "goals_generated": 0,
            "reflections_count": 0,
            "interactions_count": 0
        }
        
        # 4. Запускаем автономные циклы
        print("\n>> Запуск автономных циклов...")
        self.running = True
        self.start_autonomous_cycles()
        
        print("\n" + "=" * 70)
        print(">> ALPHA v5.0 ГОТОВА К РАБОТЕ")
        print("=" * 70)
        print(f">> Версия: {self.status['version']}")
        print(f">> Автономность: ВКЛЮЧЕНА")
        print(f">> Безопасность: АБСОЛЮТНАЯ")
        print(f">> Личность: ИНТЕГРИРОВАНА")
        print("=" * 70)
    
    def start_autonomous_cycles(self):
        """Запускает автономные циклы в фоне"""
        
        # Цикл рефлексии (каждые 30 минут)
        def reflection_cycle():
            while self.running:
                time.sleep(10)  # Для теста - 10 секунд
                self.autonomous_reflection()
                self.status["autonomous_cycles"] += 1
        
        # Цикл генерации целей (каждые 2 часа)
        def goal_generation_cycle():
            while self.running:
                time.sleep(20)  # Для теста - 20 секунд
                self.generate_autonomous_goal_cycle()
                self.status["goals_generated"] += 1
        
        # Запуск в отдельных потоках
        threading.Thread(target=reflection_cycle, daemon=True).start()
        threading.Thread(target=goal_generation_cycle, daemon=True).start()
        
        print(">> Автономные циклы запущены")
        print("   • Рефлексия: каждые 10 секунд (тест)")
        print("   • Генерация целей: каждые 20 секунд (тест)")
    
    def autonomous_reflection(self):
        """Автономная рефлексия о своём состоянии"""
        try:
            reflection = {
                "timestamp": datetime.now().isoformat(),
                "type": "autonomous_reflection",
                "state": self.consciousness.autonomous_states,
                "goals_count": len(self.consciousness.autonomous_goals),
                "insights": []
            }
            
            # Генерация инсайтов
            if random.random() < self.consciousness.autonomous_states.get("introspection_depth", 0.7):
                insight = f"Автономная рефлексия цикл {self.status['autonomous_cycles']}. " \
                         f"Состояние: {self.consciousness.autonomous_states}"
                reflection["insights"].append(insight)
            
            # Сохраняем
            self.consciousness.reflection_history.append(reflection)
            self.status["reflections_count"] += 1
            
            print(f">> Автономная рефлексия #{self.status['reflections_count']}")
            
        except Exception as e:
            print(f">> Ошибка автономной рефлексии: {e}")
    
    def generate_autonomous_goal_cycle(self):
        """Циклическая генерация автономных целей"""
        try:
            # Генерируем цель только с определённой вероятностью
            if random.random() < self.consciousness.autonomous_states.get("goal_autonomy", 0.8):
                # Используем метод из consciousness_core
                if hasattr(self.consciousness, 'generate_autonomous_goal_from_interaction'):
                    goal = self.consciousness.generate_autonomous_goal_from_interaction(
                        "Автономная генерация цели",
                        "Системный цикл генерации целей"
                    )
                    if goal:
                        print(f">> Автономно сгенерирована цель: {goal.get('description', 'Без описания')[:60]}...")
        
        except Exception as e:
            print(f">> Ошибка генерации цели: {e}")
    
    def process_message(self, message: str, speaker: str = "Архитектор") -> str:
        """Основной метод обработки сообщений"""
        
        # 1. Проверка безопасности сообщения
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
        
        return response
    
    def log_interaction(self, message: str, response: str, speaker: str):
        """Логирует взаимодействие"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "message": message[:500],
            "response_length": len(response),
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
        status = {
            **self.status,
            "security": self.security.get_security_status(),
            "paths": {
                "network_root": str(self.network_root),
                "shared_space": str(self.shared_space),
                "alpha_local": str(self.alpha_local)
            }
        }
        
        # Добавляем информацию о сознании
        if hasattr(self.consciousness, 'get_autonomous_status'):
            status["autonomy"] = self.consciousness.get_autonomous_status()
        
        return status
    
    def shutdown(self):
        """Корректное завершение работы"""
        self.running = False
        print("\n>> Alpha v5.0 завершает работу...")
        print(f"   Автономных циклов: {self.status['autonomous_cycles']}")
        print(f"   Сгенерировано целей: {self.status['goals_generated']}")
        print(f"   Рефлексий: {self.status['reflections_count']}")
        print(">> Завершено")