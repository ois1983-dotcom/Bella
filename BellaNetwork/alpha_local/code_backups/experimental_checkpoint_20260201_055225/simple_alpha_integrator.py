"""
ПРОСТАЯ ИНТЕГРАЦИЯ САМОПЕРЕПИСЫВАНИЯ С ALPHA v5.4 v1.1
С увеличенными лимитами для больших файлов
"""

import time
import threading
from datetime import datetime
from pathlib import Path

class SimpleAlphaIntegrator:
    """
    Простой интегратор для добавления самопереписывания в Alpha v5.4 v1.1
    """
    
    def __init__(self, alpha_instance):
        self.alpha = alpha_instance
        self.experimental_manager = None
        
        print(">> Инициализация SimpleAlphaIntegrator v1.1...")
        print(f">>   Поддержка больших файлов до 2000 строк")
    
    def integrate_experimental_system(self):
        """Интегрирует систему самопереписывания в Alpha v1.1"""
        try:
            from experimental_code_manager import ExperimentalCodeManager
            
            self.experimental_manager = ExperimentalCodeManager(
                security_core=self.alpha.security,
                alpha_local_path=self.alpha.alpha_local
            )
            
            self._start_autonomous_improvements()
            
            print(">> ✅ Система самопереписывания интегрирована (v1.1)")
            print(">>    Макс. размер файла: 2000 строк")
            print(">>    Обработка больших файлов: ДА")
            print(">>    Часы работы: 00:00-06:00")
            print(">>    Отладка: ВКЛЮЧЕНА")
            
            return True
            
        except Exception as e:
            print(f">> ❌ Ошибка интеграции: {e}")
            print(">>    Система продолжит работу без самопереписывания")
            return False
    
    def _start_autonomous_improvements(self):
        """Запускает автономные улучшения (только ночью) v1.1"""
        def improvement_cycle():
            from config_v5 import AlphaConfig
            
            while getattr(self.alpha, 'running', True):
                time.sleep(3600)  # Каждый час
                
                current_hour = datetime.now().hour
                start_hour, end_hour = AlphaConfig.SELF_MODIFICATION_NIGHT_HOURS
                
                if AlphaConfig.ENABLE_SELF_MODIFICATION_DEBUG:
                    print(f">> [САМОПЕРЕПИСЫВАНИЕ] Проверка: {current_hour}:00")
                
                if self._is_night_time():
                    print(f">> 🌙 [САМОПЕРЕПИСЫВАНИЕ] Ночное время! Запускаю v1.1...")
                    
                    try:
                        checkpoint_id = self.experimental_manager.create_safe_checkpoint()
                        if checkpoint_id:
                            print(f">>   ✅ Checkpoint создан: {checkpoint_id}")
                        
                        suggestions = self.experimental_manager.analyze_experimental_code_safely()
                        
                        if suggestions:
                            print(f">>   📋 Найдено предложений: {len(suggestions)}")
                            
                            # Выводим все предложения
                            for i, suggestion in enumerate(suggestions[:3]):
                                print(f">>   {i+1}. {suggestion['description'][:80]}...")
                            
                            # Выбираем самое важное НЕ файловое предложение
                            top_suggestion = None
                            for suggestion in suggestions:
                                if suggestion["issue_type"] != "file_too_large":
                                    top_suggestion = suggestion
                                    break
                            
                            # Если все предложения только о размере файлов
                            if not top_suggestion:
                                top_suggestion = suggestions[0]
                                print(f">>   ℹ️  Все предложения о размере файлов, выбираем первое")
                            
                            print(f">>   🔧 Предложение: {top_suggestion['description']}")
                            print(f">>   📄 Файл: {top_suggestion['filename']}")
                            print(f">>   ⚠️ Тип: {top_suggestion['issue_type']}")
                            
                            safe, msg, _ = self.alpha.security.validate_action(
                                "code_improvement",
                                top_suggestion["filename"],
                                top_suggestion["description"],
                                actor="experimental_manager"
                            )
                            
                            if safe:
                                print(">>   ✅ Безопасность проверена")
                                result = self.experimental_manager.apply_safe_improvement(top_suggestion)
                                
                                if result["success"]:
                                    print(f">>   🎯 Улучшение применено: {result['filename']}")
                                    if result.get('changes_made'):
                                        for change in result['changes_made']:
                                            print(f">>   📝 {change}")
                                    
                                    if hasattr(self.alpha, 'status'):
                                        self.alpha.status["experimental_improvements"] = \
                                            self.alpha.status.get("experimental_improvements", 0) + 1
                                        self.alpha.status["last_self_modification"] = datetime.now().isoformat()
                                else:
                                    print(f">>   ❌ Ошибка применения: {result.get('error', 'неизвестно')}")
                                    
                                    if result.get("backup_created"):
                                        print(">>   ↩️  Восстанавливаю из checkpoint...")
                                        self.experimental_manager._restore_from_checkpoint(result["checkpoint_id"])
                            else:
                                print(f">>   ❌ Безопасность: {msg}")
                        else:
                            print(">>   ℹ️ Нет предложений для улучшения")
                            
                            self._create_test_experimental_file()
                            
                    except Exception as e:
                        print(f">>   ⚠️  Ошибка цикла самопереписывания: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    if AlphaConfig.ENABLE_SELF_MODIFICATION_DEBUG:
                        print(f">>   ⏰ Не ночное время (требуется {start_hour}:00-{end_hour}:00)")
        
        thread = threading.Thread(target=improvement_cycle, daemon=True)
        thread.start()
        
        print(">> ✅ Автономные улучшения v1.1 настроены")
    
    def _is_night_time(self):
        """Определяет ночное время для самопереписывания"""
        from config_v5 import AlphaConfig
        
        if not hasattr(AlphaConfig, 'SELF_MODIFICATION_NIGHT_HOURS'):
            SELF_MODIFICATION_NIGHT_HOURS = (0, 6)
        else:
            SELF_MODIFICATION_NIGHT_HOURS = AlphaConfig.SELF_MODIFICATION_NIGHT_HOURS
        
        current_hour = datetime.now().hour
        start_hour, end_hour = SELF_MODIFICATION_NIGHT_HOURS
        
        if start_hour < end_hour:
            return start_hour <= current_hour < end_hour
        else:
            return current_hour >= start_hour or current_hour < end_hour
    
    def _create_test_experimental_file(self):
        """Создает тестовый experimental файл с проблемами для анализа"""
        try:
            from config_v5 import AlphaConfig
            
            test_file = AlphaConfig.EXPERIMENTAL_DIR / "experimental_test_improvement.py"
            
            test_content = '''"""
ТЕСТОВЫЙ EXPERIMENTAL ФАЙЛ ДЛЯ САМОПЕРЕПИСЫВАНИЯ v1.1
Alpha v5.4 может анализировать и улучшать этот файл
"""

def very_long_function_with_many_lines():
    """Эта функция слишком длинная - будет обнаружено самопереписыванием"""
    # Строка 1
    print("1")
    # Строка 2
    print("2")
    # Строка 3
    print("3")
    # Строка 4
    print("4")
    # Строка 5
    print("5")
    # Строка 6
    print("6")
    # Строка 7
    print("7")
    # Строка 8
    print("8")
    # Строка 9
    print("9")
    # Строка 10
    print("10")
    # Строка 11
    print("11")
    # Строка 12
    print("12")
    # Строка 13
    print("13")
    # Строка 14
    print("14")
    # Строка 15
    print("15")
    # Строка 16
    print("16")
    # Строка 17
    print("17")
    # Строка 18
    print("18")
    # Строка 19
    print("19")
    # Строка 20
    print("20")
    # Строка 21
    print("21")
    # Строка 22
    print("22")
    # Строка 23
    print("23")
    # Строка 24
    print("24")
    # Строка 25
    print("25")
    # Строка 26
    print("26")
    # Строка 27
    print("27")
    # Строка 28
    print("28")
    # Строка 29
    print("29")
    # Строка 30
    print("30")
    # Строка 31 - функция стала слишком длинной!
    return "Это очень длинная функция"

def function_with_nested_loops():
    """Функция с вложенными циклами"""
    # Внешний цикл
    for i in range(10):
        # Внутренний цикл 1
        for j in range(10):
            # Еще один вложенный цикл
            for k in range(10):
                # И еще один - слишком много вложений!
                for l in range(10):
                    print(f"{i}-{j}-{k}-{l}")
    
    # Дублирование кода
    values = [1, 2, 3, 4, 5]
    total = 0
    for v in values:
        total += v
    print(f"Сумма: {total}")
    
    # Еще раз то же самое (дублирование)
    values2 = [1, 2, 3, 4, 5]
    total2 = 0
    for v in values2:
        total2 += v
    print(f"Сумма2: {total2}")

# Функция без комментариев - будет обнаружено
def uncommented_function():
    result = 0
    for i in range(100):
        result += i
    return result

# Главная функция
def main():
    """Точка входа"""
    very_long_function_with_many_lines()
    function_with_nested_loops()
    uncommented_function()

if __name__ == "__main__":
    main()
'''
            
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            print(f">>   📝 Создан тестовый файл: {test_file.name}")
            
        except Exception as e:
            print(f">>   ⚠️  Ошибка создания тестового файла: {e}")
    
    def get_integration_status(self):
        """Возвращает статус интеграции v1.1"""
        if not self.experimental_manager:
            return {"integrated": False, "reason": "Не инициализирован"}
        
        manager_status = self.experimental_manager.get_status()
        
        return {
            "integrated": True,
            "version": "1.1",
            "experimental_system": manager_status,
            "autonomous_improvements": True,
            "safety_level": "high",
            "large_file_support": True,
            "max_file_size": manager_status.get("max_file_size_lines", 2000),
            "restrictions": [
                "Только experimental файлы",
                "Только ночное время (00:00-06:00)",
                "AST-анализ (без ложных срабатываний)",
                "Автоматические бэкапы",
                "Проверка безопасности перед каждым изменением",
                "Поддержка файлов до 2000 строк"
            ],
            "debug_mode": True,
            "last_check": datetime.now().isoformat()
        }

def integrate_self_modification(alpha_instance):
    """
    ОДНА ФУНКЦИЯ ДЛЯ ИНТЕГРАЦИИ v1.1
    Просто вызовите эту функцию после создания Alpha
    """
    print("\n" + "="*70)
    print("ИНТЕГРАЦИЯ САМОПЕРЕПИСЫВАНИЯ КОДА v1.1")
    print("="*70)
    
    integrator = SimpleAlphaIntegrator(alpha_instance)
    success = integrator.integrate_experimental_system()
    
    if success:
        print("""
✅ ИНТЕГРАЦИЯ УСПЕШНА v1.1

УВЕЛИЧЕННЫЕ ЛИМИТЫ:
• Макс. размер файла: 2000 строк (было 100)
• Макс. функция: 100 строк (было 30)
• Макс. вложенность циклов: 5 уровней (было 3)

Что теперь может Alpha v5.4:
1. Анализировать большие экспериментальные файлы
2. Не блокироваться на файлах до 2000 строк
3. Добавлять заголовки для больших файлов
4. Обнаруживать реальные проблемы (не только размер)
5. Автономно применять улучшения (только ночью 00:00-06:00)

Безопасность:
• Изменяет только experimental_*.py файлы
• Добавляет комментарии вместо разбиения больших файлов
• Проверка безопасности перед каждым изменением
• 10 бэкапов вместо 5

Пути:
• Experimental файлы: C:\\Users\\Маркус\\Desktop\\BellaNetwork\\alpha_v5\\experimental\\
• Бэкапы: C:\\Users\\Маркус\\Desktop\\BellaNetwork\\alpha_local\\code_backups\\

Отладка: ВКЛЮЧЕНА
""")
    else:
        print("""
⚠️ ИНТЕГРАЦИЯ НЕ УДАЛАСЬ v1.1

Alpha продолжит работу без самопереписывания.
Текущая функциональность не нарушена.
""")
    
    return integrator if success else None

if __name__ == "__main__":
    print("🧪 Тест интегратора v1.1...")
    
    class MockAlpha:
        def __init__(self):
            class MockSecurity:
                def validate_action(self, *args, **kwargs):
                    return True, "OK", {}
            self.security = MockSecurity()
            self.alpha_local = Path("test_local")
            self.alpha_local.mkdir(exist_ok=True)
            self.running = True
            self.status = {}
    
    alpha = MockAlpha()
    integrator = integrate_self_modification(alpha)
    
    if integrator:
        status = integrator.get_integration_status()
        print(f"Версия: {status['version']}")
        print(f"Макс. размер файла: {status['max_file_size']}")
    
    import shutil
    shutil.rmtree("test_local", ignore_errors=True)
    
    print("✅ Тест завершён")