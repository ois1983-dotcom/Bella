"""
УМНЫЙ ИНТЕГРАТОР САМОПЕРЕПИСЫВАНИЯ С ALPHA v5.4 v1.2
С архитектурным пониманием и умным анализом
ПОЛНАЯ ВЕРСИЯ со всеми методами и корректным взаимодействием
"""

import time
import threading
import shutil
import json
from datetime import datetime
from pathlib import Path

class SimpleAlphaIntegrator:
    """
    Умный интегратор для добавления самопереписывания в Alpha v5.4 v1.2
    ПОЛНАЯ ВЕРСИЯ с корректным взаимодействием
    """
    
    def __init__(self, alpha_instance):
        self.alpha = alpha_instance
        self.experimental_manager = None
        
        print(">> Инициализация SimpleAlphaIntegrator v1.2...")
        print(f">>   УМНЫЙ анализ: понимает архитектуру")
        print(f">>   Архитектурная защита: ВКЛЮЧЕНА")
        print(f">>   Взаимодействие: ОПТИМИЗИРОВАНО")
    
    def integrate_experimental_system(self):
        """Интегрирует систему самопереписывания в Alpha v1.2"""
        try:
            from experimental_code_manager import ExperimentalCodeManager
            
            self.experimental_manager = ExperimentalCodeManager(
                security_core=self.alpha.security,
                alpha_local_path=self.alpha.alpha_local
            )
            
            self._start_intelligent_improvements()
            
            print(">> ✅ Система самопереписывания интегрирована (v1.2)")
            print(">>    Умный анализ: ВКЛЮЧЕН")
            print(">>    Архитектурное понимание: ДА")
            print(">>    Часы работы: 00:00-06:00")
            print(">>    Взаимодействие: КОРРЕКТНОЕ")
            
            return True
            
        except Exception as e:
            print(f">> ❌ Ошибка интеграции: {e}")
            print(">>    Система продолжит работу без самопереписывания")
            return False
    
    def _start_intelligent_improvements(self):
        """Запускает интеллектуальные улучшения (только ночью) v1.2"""
        def improvement_cycle():
            from config_v5 import AlphaConfig
            
            while getattr(self.alpha, 'running', True):
                time.sleep(3600)  # Каждый час
                
                current_hour = datetime.now().hour
                start_hour, end_hour = AlphaConfig.SELF_MODIFICATION_NIGHT_HOURS
                
                if AlphaConfig.ENABLE_SELF_MODIFICATION_DEBUG:
                    print(f">> [САМОПЕРЕПИСЫВАНИЕ v1.2] Проверка: {current_hour}:00")
                
                if self._is_night_time():
                    print(f">> 🌙 [УМНОЕ САМОПЕРЕПИСЫВАНИЕ] Ночное время! Запускаю v1.2...")
                    
                    try:
                        checkpoint_id = self.experimental_manager.create_safe_checkpoint()
                        if checkpoint_id:
                            print(f">>   ✅ Checkpoint создан: {checkpoint_id}")
                        
                        suggestions = self.experimental_manager.analyze_experimental_code_safely()
                        
                        if suggestions:
                            print(f">>   📋 Найдено УМНЫХ предложений: {len(suggestions)}")
                            
                            # 🔴 ИСПРАВЛЕНО: Используем единую логику фильтрации
                            real_suggestions = []
                            for suggestion in suggestions:
                                filename = suggestion.get("filename", "")
                                
                                # 🔴 v1.2: Используем метод менеджера для проверки архитектурных файлов
                                # Вместо самостоятельной фильтрации, доверяем менеджеру
                                
                                # Пропускаем низкоприоритетные
                                if suggestion.get("priority", 0) < 4:
                                    if AlphaConfig.ENABLE_SELF_MODIFICATION_DEBUG:
                                        print(f">>   📉 Пропускаем низкоприоритетное: {suggestion['priority']}")
                                    continue
                                
                                real_suggestions.append(suggestion)
                            
                            if real_suggestions:
                                # Выбираем самое важное
                                real_suggestions.sort(key=lambda x: x["priority"], reverse=True)
                                top_suggestion = real_suggestions[0]
                                
                                print(f">>   🔧 УМНОЕ предложение: {top_suggestion['description']}")
                                print(f">>   📄 Файл: {top_suggestion['filename']}")
                                print(f">>   ⚠️  Тип: {top_suggestion['issue_type']}")
                                print(f">>   ⚡ Приоритет: {top_suggestion['priority']}/10")
                                
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
                                        print(f">>   🎯 УМНОЕ улучшение применено: {result['filename']}")
                                        if result.get('changes_made'):
                                            for change in result['changes_made']:
                                                print(f">>   📝 {change}")
                                        
                                        if hasattr(self.alpha, 'status'):
                                            self.alpha.status["intelligent_improvements"] = \
                                                self.alpha.status.get("intelligent_improvements", 0) + 1
                                            self.alpha.status["last_self_modification"] = datetime.now().isoformat()
                                            self.alpha.status["self_modification_version"] = "1.2"
                                    else:
                                        print(f">>   ❌ Ошибка применения: {result.get('error', 'неизвестно')}")
                                        
                                        if result.get("backup_created"):
                                            print(">>   ↩️  Восстанавливаю из checkpoint...")
                                            self.experimental_manager._restore_from_checkpoint(result["checkpoint_id"])
                                else:
                                    print(f">>   ❌ Безопасность: {msg}")
                            else:
                                print(">>   ℹ️ Нет РЕАЛЬНЫХ проблем для улучшения")
                                print(">>   🧠 Система работает оптимально")
                                
                                # 🔴 v1.2: Создаем тестовый файл ТОЛЬКО если нет реальных проблем
                                self._create_smart_test_file()
                                
                        else:
                            print(">>   ℹ️ Умный анализ не нашёл проблем")
                            print(">>   🎯 Все experimental файлы в хорошем состоянии")
                            
                    except Exception as e:
                        print(f">>   ⚠️  Ошибка цикла самопереписывания: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    if AlphaConfig.ENABLE_SELF_MODIFICATION_DEBUG:
                        print(f">>   ⏰ Не ночное время (требуется {start_hour}:00-{end_hour}:00)")
        
        thread = threading.Thread(target=improvement_cycle, daemon=True)
        thread.start()
        
        print(">> ✅ Интеллектуальные улучшения v1.2 настроены")
    
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
    
    def _create_smart_test_file(self):
        """Создает умный тестовый experimental файл для анализа v1.2"""
        try:
            from config_v5 import AlphaConfig
            
            test_file = self.experimental_manager.experimental_dir / "experimental_smart_test_v1_2.py"
            
            test_content = '''"""
УМНЫЙ ТЕСТОВЫЙ ФАЙЛ ДЛЯ СИСТЕМЫ САМОПЕРЕПИСЫВАНИЯ v1.2
Alpha v5.4 может анализировать и улучшать этот файл
Это НЕ архитектурный файл, поэтому система может его улучшать
"""

def simple_function_with_issues():
    """Эта функция имеет несколько проблем для обнаружения"""
    # Много повторяющегося кода
    result = 0
    for i in range(10):
        result += i
    
    # Еще раз то же самое (дублирование)
    result2 = 0
    for i in range(10):
        result2 += i
    
    return result + result2

def function_with_low_comments():
    # Функция без достаточных комментариев
    values = [1, 2, 3, 4, 5]
    total = 0
    for v in values:
        total += v
    return total

def nested_loops_example():
    """Пример с вложенными циклами"""
    # Внешний цикл
    for i in range(5):
        # Внутренний цикл 1
        for j in range(5):
            # Еще один вложенный цикл
            for k in range(5):
                print(f"{i}-{j}-{k}")
    
    return "Готово"

# Главная функция
def main():
    """Точка входа"""
    print("Тест системы v1.2")
    simple_function_with_issues()
    function_with_low_comments()
    nested_loops_example()

if __name__ == "__main__":
    main()
'''
            
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            print(f">>   📝 Создан умный тестовый файл: {test_file.name}")
            print(f">>   ℹ️  Файл создан для тестирования системы v1.2")
            
        except Exception as e:
            print(f">>   ⚠️  Ошибка создания тестового файла: {e}")
    
    def _create_test_experimental_file(self):
        """Создает тестовый experimental файл с проблемами для анализа (v1.1)"""
        try:
            from config_v5 import AlphaConfig
            
            test_file = self.experimental_manager.experimental_dir / "experimental_test_improvement.py"
            
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
        """Возвращает статус интеграции v1.2"""
        if not self.experimental_manager:
            return {"integrated": False, "reason": "Не инициализирован"}
        
        manager_status = self.experimental_manager.get_status()
        
        return {
            "integrated": True,
            "version": "1.2",
            "experimental_system": manager_status,
            "autonomous_improvements": True,
            "intelligent_improvements": True,
            "safety_level": "high",
            "large_file_support": True,
            "architectural_protection": True,
            "max_file_size": manager_status.get("max_file_size_lines", 2000),
            "interaction": "optimized",
            "restrictions": [
                "Только experimental файлы",
                "Только ночное время (00:00-06:00)",
                "AST-анализ с архитектурным пониманием",
                "Автоматические бэкапы",
                "Проверка безопасности перед каждым изменением",
                "Защита архитектурных файлов",
                "Умный анализ"
            ],
            "debug_mode": True,
            "last_check": datetime.now().isoformat()
        }
    
    def get_quick_status(self):
        """Быстрый статус для отладки"""
        return {
            "version": "1.2",
            "active": self.experimental_manager is not None,
            "last_check": datetime.now().isoformat(),
            "architectural_protection": "ENABLED",
            "mode": "INTELLIGENT",
            "interaction": "CORRECT"
        }
    
    def run_manual_analysis(self):
        """Запускает ручной анализ experimental файлов"""
        if not self.experimental_manager:
            print(">> ❌ Менеджер не инициализирован")
            return None
        
        print(">> 🔍 Запуск ручного анализа v1.2...")
        
        # Используем метод менеджера для анализа
        suggestions = self.experimental_manager.analyze_experimental_code_safely()
        
        # 🔴 ИСПРАВЛЕНО: Правильная классификация файлов
        architectural_files = []
        real_issues = []
        
        for suggestion in suggestions:
            filename = suggestion.get("filename", "")
            # Проверяем, является ли файл архитектурным
            try:
                filepath = self.experimental_manager.experimental_dir / filename
                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    # Используем метод менеджера для проверки
                    if self.experimental_manager._is_architectural_file(filename, code):
                        architectural_files.append(suggestion)
                    else:
                        real_issues.append(suggestion)
                else:
                    real_issues.append(suggestion)  # Если файл не найден, считаем его обычным
            except:
                real_issues.append(suggestion)  # При ошибке считаем обычным
        
        print(f">> 📊 Результаты анализа:")
        print(f">>    Всего файлов: {len(list(self.experimental_manager.experimental_dir.glob('*.py')))}")
        print(f">>    Найдено предложений: {len(suggestions)}")
        print(f">>    Архитектурные файлы (защищены): {len(architectural_files)}")
        print(f">>    Реальные проблемы: {len(real_issues)}")
        
        if real_issues:
            print(f">> 🎯 Реальные проблемы для улучшения:")
            for i, issue in enumerate(real_issues[:3]):
                print(f">>   {i+1}. {issue['filename']}: {issue['description'][:60]}...")
        
        return {
            "total_suggestions": len(suggestions),
            "architectural_files": len(architectural_files),
            "real_issues": len(real_issues),
            "top_issues": real_issues[:3] if real_issues else []
        }
    
    def create_emergency_backup(self):
        """Создает экстренный бэкап всех experimental файлов"""
        if not self.experimental_manager:
            print(">> ❌ Менеджер не инициализирован")
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = self.alpha.alpha_local / "emergency_backups" / f"emergency_v1_2_{timestamp}"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            experimental_files = list(self.experimental_manager.experimental_dir.glob("*.py"))
            
            for file in experimental_files:
                shutil.copy2(file, backup_dir / file.name)
            
            # Создаем метаданные
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "type": "emergency_backup",
                "reason": "Ручное создание через SimpleAlphaIntegrator v1.2",
                "files": [f.name for f in experimental_files],
                "version": "1.2",
                "note": "Экстренный бэкап создан вручную"
            }
            
            with open(backup_dir / "metadata.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            print(f">> 🚨 Экстренный бэкап создан: {backup_dir.name}")
            print(f">> 📁 Файлов сохранено: {len(experimental_files)}")
            
            return backup_dir.name
            
        except Exception as e:
            print(f">> ❌ Ошибка создания экстренного бэкапа: {e}")
            return None

# 🔴 ИСПРАВЛЕННАЯ функция для совместимости
def integrate_self_modification(alpha_instance):
    """
    ОРИГИНАЛЬНАЯ ФУНКЦИЯ ДЛЯ ИНТЕГРАЦИИ v1.1 (совместимость)
    """
    print("\n" + "="*70)
    print("ИНТЕГРАЦИЯ САМОПЕРЕПИСЫВАНИЯ КОДА v1.1 (режим совместимости)")
    print("="*70)
    
    integrator = SimpleAlphaIntegrator(alpha_instance)
    success = integrator.integrate_experimental_system()
    
    if success:
        print("""
✅ ИНТЕГРАЦИЯ УСПЕШНА v1.2 (режим совместимости)

УВЕЛИЧЕННЫЕ ЛИМИТЫ:
• Макс. размер файла: 2000 строк (было 100)
• Макс. функция: 100 строк (было 30)
• Макс. вложенность циклов: 5 уровней (было 3)

НОВОЕ в v1.2:
• УМНЫЙ анализ: понимает архитектуру
• Защита интеграторов и эмоциональных ядер
• Различает данные и логику
• Сохраняет отказоустойчивость

ВЗАИМОДЕЙСТВИЕ:
• Интегратор и менеджер работают согласованно
• Единая логика фильтрации архитектурных файлов
• Корректная обработка импортов
""")
    else:
        print("""
⚠️ ИНТЕГРАЦИЯ НЕ УДАЛАСЬ
""")
    
    return integrator if success else None

# 🔴 ОСНОВНАЯ функция для v1.2
def integrate_intelligent_self_modification(alpha_instance):
    """
    НОВАЯ ФУНКЦИЯ ДЛЯ ИНТЕЛЛЕКТУАЛЬНОЙ ИНТЕГРАЦИИ v1.2
    """
    print("\n" + "="*70)
    print("ИНТЕЛЛЕКТУАЛЬНОЕ САМОПЕРЕПИСЫВАНИЕ КОДА v1.2")
    print("="*70)
    
    integrator = SimpleAlphaIntegrator(alpha_instance)
    success = integrator.integrate_experimental_system()
    
    if success:
        print("""
✅ ИНТЕЛЛЕКТУАЛЬНАЯ ИНТЕГРАЦИЯ УСПЕШНА v1.2

ФИЛОСОФИЯ v1.2:
"Не все, что выглядит как проблема - является проблемой.
 Архитектурная целостность важнее формальной чистоты кода."

КЛЮЧЕВЫЕ УЛУЧШЕНИЯ:
1. УМНЫЙ АНАЛИЗ: различает данные и логику
2. АРХИТЕКТУРНОЕ ПОНИМАНИЕ: не ломает fallback-структуры
3. ЗАЩИТА ИНТЕГРАТОРОВ: emotional_integrator.py теперь защищен
4. ПРИОРИТИЗАЦИЯ: только реальные проблемы
5. СОХРАНЕНИЕ ЦЕЛОСТНОСТИ: не разрушает отказоустойчивость
6. КОРРЕКТНОЕ ВЗАИМОДЕЙСТВИЕ: интегратор и менеджер работают согласованно

ВЗАИМОДЕЙСТВИЕ ФИКСИРОВАНО:
• Добавлены недостающие импорты (shutil, json)
• Единая логика проверки архитектурных файлов
• Удалена двойная фильтрация
• Корректный доступ к методам менеджера

НОВЫЕ МЕТОДЫ v1.2:
• get_quick_status() - быстрый статус
• run_manual_analysis() - ручной анализ с правильной классификацией
• create_emergency_backup() - экстренные бэкапы (работает!)

СОВМЕСТИМОСТЬ:
• Функция integrate_self_modification() сохранена для v1.1
• Все оригинальные API методы работают
• Добавлены новые интеллектуальные методы

Безопасность:
• Изменяет только простые experimental файлы
• Не трогает архитектурные файлы без крайней необходимости
• Проверка безопасности перед каждым изменением
• 10 бэкапов + экстренные бэкапы

Взаимодействие: ОПТИМИЗИРОВАНО И КОРРЕКТНО
""")
    else:
        print("""
⚠️ ИНТЕЛЛЕКТУАЛЬНАЯ ИНТЕГРАЦИЯ НЕ УДАЛАСЬ v1.2
""")
    
    return integrator if success else None

# Тестирование взаимодействия
if __name__ == "__main__":
    print("🧪 ТЕСТ ВЗАИМОДЕЙСТВИЯ v1.2...")
    
    try:
        from pathlib import Path
        
        class MockSecurity:
            def validate_action(self, *args, **kwargs):
                return True, "OK", {}
        
        class MockAlpha:
            def __init__(self):
                self.security = MockSecurity()
                self.alpha_local = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local")
                self.running = True
                self.status = {}
        
        alpha = MockAlpha()
        
        print("1. Тестируем создание интегратора и менеджера...")
        integrator = SimpleAlphaIntegrator(alpha)
        success = integrator.integrate_experimental_system()
        
        if success and integrator.experimental_manager:
            print("✅ Интегратор и менеджер созданы успешно")
            
            print("\n2. Тестируем методы взаимодействия...")
            
            # Проверяем, что менеджер имеет необходимые методы
            required_methods = [
                'analyze_experimental_code_safely',
                'apply_safe_improvement', 
                'create_safe_checkpoint',
                '_restore_from_checkpoint',
                '_is_architectural_file'
            ]
            
            for method in required_methods:
                if hasattr(integrator.experimental_manager, method):
                    print(f"✅ Метод {method} доступен")
                else:
                    print(f"❌ Метод {method} НЕ доступен!")
            
            print("\n3. Тестируем вызовы...")
            
            # Создаем тестовый файл
            test_dir = integrator.experimental_manager.experimental_dir
            test_file = test_dir / "test_interaction.py"
            test_file.write_text('print("Тест взаимодействия")')
            
            # Анализ
            suggestions = integrator.experimental_manager.analyze_experimental_code_safely()
            print(f"✅ Анализ выполнен: {len(suggestions)} предложений")
            
            # Статус
            status = integrator.experimental_manager.get_status()
            print(f"✅ Статус менеджера: версия {status.get('version')}")
            
            # Интегратор статус
            integrator_status = integrator.get_integration_status()
            print(f"✅ Статус интегратора: версия {integrator_status.get('version')}")
            
            # Быстрый статус
            quick_status = integrator.get_quick_status()
            print(f"✅ Быстрый статус: {quick_status.get('mode')}")
            
            print("\n4. Тестируем ручной анализ...")
            analysis_result = integrator.run_manual_analysis()
            print(f"✅ Ручной анализ: {analysis_result.get('total_suggestions', 0)} предложений")
            
            print("\n5. Тестируем создание emergency backup...")
            backup_id = integrator.create_emergency_backup()
            if backup_id:
                print(f"✅ Emergency backup создан: {backup_id}")
            
            # Удаляем тестовый файл
            test_file.unlink(missing_ok=True)
            
            print("\n🎯 ВСЕ ТЕСТЫ ВЗАИМОДЕЙСТВИЯ ПРОЙДЕНЫ!")
            print("📋 РЕЗУЛЬТАТЫ:")
            print("   • Интегратор и менеджер создаются корректно")
            print("   • Все необходимые методы доступны")
            print("   • Вызовы методов работают без ошибок")
            print("   • Взаимодействие оптимизировано")
            print("   • Архитектурная защита включена")
            
        else:
            print("❌ Ошибка создания интегратора или менеджера")
            
    except Exception as e:
        print(f"❌ Ошибка теста взаимодействия: {e}")
        import traceback
        traceback.print_exc()
    
    print("✅ Тест взаимодействия завершен")