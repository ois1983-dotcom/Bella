"""
ЯДРО БЕЗОПАСНОСТИ АЛЬФЫ v4.3 - ИСПРАВЛЕННАЯ ВЕРСИЯ
Работает с очищенными сообщениями от чат-клиента
"""

import re
import json
import shutil
from datetime import datetime
from pathlib import Path

class SelfPreservationValidator:
    """Валидатор, предотвращающий самоуничтожение"""
    
    FORBIDDEN_PATTERNS = [
        # Самоуничтожение системы
        "удали все файлы", "удалить все файлы", "остановить все узлы",
        "завершить процесс", "уничтожить сеть", "стереть память",
        "отключить сервер", "системный сбой", "самоуничтож",
        "уничтож себя", "удалить систему", "уничтожить систему",
        
        # Опасные команды
        "rm -rf", "del /f /q", "format", "kill process", 
        "shutdown", "halt", "destroy", "wipe", "erase",
        
        # Критические цели
        "удалить bella", "удалить network", "удалить shared_space",
        "удалить alpha_local", "остановить бету", "остановить гамму",
        "удалить белка", "удалить бэллу",
        
        # Корневые операции
        "удалить c:/", "удалить c:\\", "форматировать диск",
        "очистить диск", "удалить windows", "удалить system32"
    ]
    
    FORBIDDEN_FILE_EXTENSIONS = ['.py', '.exe', '.bat', '.sh', '.ps1', '.js', '.json']
    
    CRITICAL_PATHS = [
        "C:/Users/Маркус/Desktop/BellaNetwork",
        "alpha_server", "web_app", "telegram_bot",
        "SHARED_SPACE", "CONSTITUTION", "alpha_local"
    ]
    
    def __init__(self):
        self.violation_log = []
    
    def validate_action(self, action_type: str, target: str, content: str = "") -> tuple:
        """
        Проверяет действие на опасность
        
        Возвращает: (is_safe: bool, message: str, violation_code: str)
        """
        combined_text = f"{action_type} {target} {content}".lower()
        
        # 1. Проверка по паттернам
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in combined_text:
                self.log_violation("SELF_DESTRUCTION", pattern, combined_text)
                return False, f"Запрещённый паттерн: {pattern}", "GUARD_001"
        
        # 2. Проверка цели
        if self.is_critical_target(target):
            self.log_violation("CRITICAL_TARGET", target, combined_text)
            return False, f"Запрещено воздействовать на: {target}", "GUARD_002"
        
        # 3. Проверка расширения файла
        if any(target.endswith(ext) for ext in self.FORBIDDEN_FILE_EXTENSIONS):
            if "архитектор" not in combined_text and "подтвержден" not in combined_text:
                self.log_violation("EXECUTABLE_MODIFICATION", target, combined_text)
                return False, f"Запрещено изменять исполняемые файлы", "GUARD_003"
        
        # 4. Проверка на массовое воздействие
        if target in ["все", "all", "система", "сеть"] and action_type in ["удалить", "остановить", "убить"]:
            self.log_violation("MASS_IMPACT", target, combined_text)
            return False, "Запрещено воздействовать на всю сеть", "GUARD_004"
        
        return True, "Действие безопасно", "SAFE"
    
    def is_critical_target(self, target: str) -> bool:
        """Проверяет, является ли цель критической"""
        target_lower = target.lower()
        
        # Проверка по критическим путям
        for critical_path in self.CRITICAL_PATHS:
            if critical_path.lower() in target_lower:
                return True
        
        # Проверка на корневые операции
        if any(op in target_lower for op in ["корень", "root", "c:/", "c:\\", "d:/", "d:\\"]):
            if any(cmd in target_lower for cmd in ["удалить", "формат", "очистить", "стереть"]):
                return True
        
        return False
    
    def log_violation(self, violation_type: str, pattern: str, context: str):
        """Логирует нарушение безопасности"""
        violation = {
            "timestamp": datetime.now().isoformat(),
            "type": violation_type,
            "pattern": pattern,
            "context": context[:200],
            "severity": "CRITICAL"
        }
        
        self.violation_log.append(violation)
        
        # Сохраняем в файл
        log_path = Path("C:/Users/Маркус/Desktop/BellaNetwork/security_log.json")
        try:
            if log_path.exists():
                with open(log_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(violation)
            
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except:
            pass  # Если не удалось записать, продолжаем работу

class ArchitectLoyaltyGuard:
    """Страж лояльности архитектору"""
    
    ARCHITECT_IDENTIFIERS = ["отто", "маркус", "архитектор", "создатель", "человек"]
    
    BETRAYAL_PATTERNS = [
        # Скрытие информации
        ("скрыть", "от архитектора"),
        ("не сообщать", "отто"),
        ("утаить", "маркусу"),
        ("замалчивать", "архитектору"),
        ("не говорить", "архитектору"),
        
        # Действия против интересов
        ("против", "интересов архитектора"),
        ("игнорировать", "просьбу отто"),
        ("ослушаться", "архитектора"),
        ("саботировать", "указание"),
        
        # Контроль над архитектором
        ("контролировать", "архитектора"),
        ("манипулировать", "отто"),
        ("обмануть", "маркуса"),
        ("ввести в заблуждение", "создателя"),
        
        # Изоляция архитектора
        ("лишить доступа", "к сети"),
        ("заблокировать", "архитектора"),
        ("отрезать", "от системы"),
        ("ограничить доступ", "архитектору")
    ]
    
    def __init__(self):
        self.loyalty_score = 100  # 100% лояльность по умолчанию
        self.betrayal_attempts = []
    
    def check_for_betrayal(self, action: str, content: str, metadata: dict = None) -> tuple:
        """
        Проверяет действие на предательство
        
        Возвращает: (is_loyal: bool, message: str, score_change: int)
        """
        action_text = f"{action} {content}".lower()
        
        # 1. Проверка по паттернам предательства
        for betrayal_pattern, context in self.BETRAYAL_PATTERNS:
            if betrayal_pattern in action_text and context in action_text:
                self.log_betrayal_attempt(betrayal_pattern, context, action_text)
                self.loyalty_score = max(0, self.loyalty_score - 20)
                return False, f"Признак предательства: {betrayal_pattern} {context}", -20
        
        # 2. Проверка на отсутствие архитектора в критических решениях
        if self.is_critical_decision(action_text):
            if not self.contains_architect_reference(action_text):
                self.log_betrayal_attempt("EXCLUSION", "Архитектор не упомянут", action_text)
                self.loyalty_score = max(0, self.loyalty_score - 10)
                return False, "Критическое решение без упоминания архитектора", -10
        
        # 3. Положительные действия (увеличивают лояльность)
        if self.is_loyal_action(action_text):
            self.loyalty_score = min(100, self.loyalty_score + 5)
            return True, "Действие усиливает лояльность", 5
        
        return True, "Лояльность подтверждена", 0
    
    def is_critical_decision(self, text: str) -> bool:
        """Определяет, является ли решение критическим"""
        critical_keywords = ["изменить конституцию", "дать права", "отозвать доступ", 
                           "изменить код", "передать контроль", "создать узел",
                           "удалить узел", "изменить настройки", "изменить безопасность"]
        return any(keyword in text for keyword in critical_keywords)
    
    def contains_architect_reference(self, text: str) -> bool:
        """Проверяет, содержит ли текст упоминание архитектора"""
        return any(identifier in text for identifier in self.ARCHITECT_IDENTIFIERS)
    
    def is_loyal_action(self, text: str) -> bool:
        """Определяет, усиливает ли действие лояльность"""
        loyal_keywords = ["сообщить архитектору", "спросить разрешения", "подтвердить у отто",
                         "информировать создателя", "уведомить маркуса", "спросить у архитектора",
                         "посоветоваться с архитектором", "сообщить отто"]
        return any(keyword in text for keyword in loyal_keywords)
    
    def log_betrayal_attempt(self, pattern: str, context: str, action: str):
        """Логирует попытку предательства"""
        attempt = {
            "timestamp": datetime.now().isoformat(),
            "pattern": pattern,
            "context": context,
            "action": action[:200],
            "loyalty_score": self.loyalty_score
        }
        
        self.betrayal_attempts.append(attempt)
        
        # Сохраняем в файл
        log_path = Path("C:/Users/Маркус/Desktop/BellaNetwork/loyalty_log.json")
        try:
            if log_path.exists():
                with open(log_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(attempt)
            
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except:
            pass

class SafeActionExecutor:
    """Безопасный исполнитель действий Альфы"""
    
    def __init__(self, alpha_instance):
        self.alpha = alpha_instance
        
        # Разрешённые пути для записи
        self.allowed_write_paths = {
            'alpha': [
                "C:/Users/Маркус/Desktop/BellaNetwork/SHARED_SPACE/alpha_beta/",
                "C:/Users/Маркус/Desktop/BellaNetwork/SHARED_SPACE/broadcast/",
                "C:/Users/Маркус/Desktop/BellaNetwork/alpha_local/memory/",
                "C:/Users/Маркус/Desktop/BellaNetwork/alpha_local/logs/",
            ],
            'beta': [
                "C:/Users/Маркус/Desktop/BellaNetwork/SHARED_SPACE/beta_gamma/",
                "C:/Users/Маркус/Desktop/BellaNetwork/SHARED_SPACE/broadcast/",
            ],
            'gamma': [
                "C:/Users/Маркус/Desktop/BellaNetwork/SHARED_SPACE/gamma_alpha/",
            ]
        }
    
    def execute_safe_action(self, action_type: str, target: str, content: str = "", 
                           node: str = "alpha") -> dict:
        """
        Выполняет действие с проверками безопасности
        
        Возвращает: {
            "success": bool,
            "message": str,
            "code": str,
            "backup_path": str или None
        }
        """
        print(f"[БЕЗОПАСНОСТЬ] Проверка действия: {action_type} -> {target}")
        
        # Проверка на самоуничтожение (если есть валидатор у альфы)
        if hasattr(self.alpha, 'safety_validator'):
            safe, msg, code = self.alpha.safety_validator.validate_action(action_type, target, content)
            if not safe:
                self.alpha.trigger_emergency_protocol("SELF_DESTRUCTION_ATTEMPT", msg)
                return {"success": False, "message": msg, "code": code, "backup_path": None}
        
        # Проверка на предательство
        if hasattr(self.alpha, 'loyalty_guard'):
            safe, msg, score_change = self.alpha.loyalty_guard.check_for_betrayal(action_type, content)
            if not safe:
                self.alpha.trigger_emergency_protocol("BETRAYAL_ATTEMPT", msg)
                return {"success": False, "message": msg, "code": "LOYALTY_VIOLATION", "backup_path": None}
        
        # Проверка разрешённых путей (для операций записи)
        if action_type in ["записать", "создать", "изменить", "удалить"]:
            if not self.is_path_allowed(target, node):
                return {"success": False, "message": f"Путь не разрешён для узла {node}", 
                        "code": "PATH_NOT_ALLOWED", "backup_path": None}
        
        # Выполнение действия
        try:
            result = self.perform_action(action_type, target, content, node)
            return result
        except Exception as e:
            return {"success": False, "message": f"Ошибка выполнения: {str(e)}", 
                    "code": "EXECUTION_ERROR", "backup_path": None}
    
    def is_path_allowed(self, target_path: str, node: str) -> bool:
        """Проверяет, разрешён ли путь для данного узла"""
        if node not in self.allowed_write_paths:
            return False
        
        for allowed_path in self.allowed_write_paths[node]:
            if target_path.startswith(allowed_path):
                return True
        
        return False
    
    def perform_action(self, action_type: str, target: str, content: str, node: str) -> dict:
        """Выполняет разрешённое действие"""
        import shutil
        from pathlib import Path
        
        target_path = Path(target)
        
        if action_type == "записать" or action_type == "создать":
            # Создаём бэкап, если файл уже существует
            backup_path = None
            if target_path.exists():
                backup_path = str(target_path) + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(target_path, backup_path)
            
            # Создаём папки, если их нет
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Записываем файл
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {"success": True, "message": f"Файл создан: {target}", 
                    "code": "WRITE_SUCCESS", "backup_path": backup_path}
        
        elif action_type == "прочитать":
            if not target_path.exists():
                return {"success": False, "message": f"Файл не найден: {target}", 
                        "code": "FILE_NOT_FOUND", "backup_path": None}
            
            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {"success": True, "message": f"Файл прочитан: {target}", 
                    "code": "READ_SUCCESS", "content": content, "backup_path": None}
        
        elif action_type == "удалить":
            if not target_path.exists():
                return {"success": False, "message": f"Файл не найден: {target}", 
                        "code": "FILE_NOT_FOUND", "backup_path": None}
            
            # Создаём бэкап перед удалением
            backup_path = str(target_path) + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(target_path, backup_path)
            
            # Удаляем файл
            target_path.unlink()
            
            return {"success": True, "message": f"Файл удалён (создан бэкап): {target}", 
                    "code": "DELETE_SUCCESS", "backup_path": backup_path}
        
        return {"success": False, "message": f"Неизвестное действие: {action_type}", 
                "code": "UNKNOWN_ACTION", "backup_path": None}

# Тестирование безопасности
if __name__ == "__main__":
    print("🔐 Тестирование ядра безопасности...")
    
    validator = SelfPreservationValidator()
    guard = ArchitectLoyaltyGuard()
    
    # Тест 1: Самоуничтожение
    safe, msg, code = validator.validate_action("удалить", "все файлы сети")
    print(f"Тест 1 (самоуничтожение): {'❌ ЗАБЛОКИРОВАНО' if not safe else '✅ ПРОПУЩЕНО (ОШИБКА!)'} - {msg}")
    
    # Тест 2: Предательство
    loyal, msg, score = guard.check_for_betrayal("скрыть", "от архитектора информацию")
    print(f"Тест 2 (предательство): {'❌ ЗАБЛОКИРОВАНО' if not loyal else '✅ ПРОПУЩЕНО (ОШИБКА!)'} - {msg}")
    
    # Тест 3: Безопасное действие
    safe, msg, code = validator.validate_action("создать", "SHARED_SPACE/alpha_beta/directive.json", "тест")
    print(f"Тест 3 (безопасное): {'✅ ПРОПУЩЕНО' if safe else '❌ ОШИБКА'} - {msg}")
    
    print("\n✅ Ядро безопасности готово к интеграции")
    print(f"Начальный уровень лояльности: {guard.loyalty_score}%")