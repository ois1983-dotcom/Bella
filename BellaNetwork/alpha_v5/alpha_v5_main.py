"""
ALPHA V5.4 - ПОЛНЫЙ OLLAMA РЕЖИМ С ИНТЕРНЕТОМ И ЭМОЦИОНАЛЬНЫМ КОНТЕКСТОМ
С ИНТЕГРАЦИЕЙ ДОСТУПА К ИНТЕРНЕТУ ЧЕРЕЗ WIKIPEDIA API
"""

import sys
from pathlib import Path
import threading
import time
from datetime import datetime
import json
import random
from typing import Dict
import subprocess
import os

sys.path.append(str(Path(__file__).parent))

from improved_security_core import ImmutableSecurityCore
from consciousness_core_v5_3 import DynamicConsciousness as AutonomousConsciousness
from config_v5 import AlphaConfig
from persistent_core import PersistentCore

class AlphaV5_4:
    """Основной класс Alpha v5.4 - ТОЛЬКО OLLAMA с интернетом и эмоциональным контекстом"""
    
    def __init__(self, network_root: Path, dialog_files: list):
        print("=" * 70)
        print(">> ЗАПУСК ALPHA v5.4 - ПОЛНЫЙ OLLAMA РЕЖИМ С ИНТЕРНЕТОМ")
        print(">> И ЭМОЦИОНАЛЬНЫМ КОНТЕКСТОМ")
        print("=" * 70)
        print(">> ВНИМАНИЕ: Все ответы будут генерироваться Ollama")
        print(">>          Время ответа может быть долгим (до 10 минут)")
        print(">>          Доступ к интернету через Wikipedia API ")
        print("=" * 70)
        
        self.network_root = network_root
        self.shared_space = network_root / "SHARED_SPACE"
        self.alpha_local = network_root / "alpha_local"
        
        self.shared_space.mkdir(exist_ok=True)
        self.alpha_local.mkdir(exist_ok=True)
        
        print(f">> Сеть: {self.network_root}")
        print(f">> SHARED_SPACE: {self.shared_space}")
        print(f">> ALPHA_LOCAL: {self.alpha_local}")
        
        # 1. Статус системы
        self.status = {
            "version": "5.4",
            "started_at": datetime.now().isoformat(),
            "autonomous_cycles": 0,
            "security_violations": 0,
            "interactions_count": 0,
            "nightly_reflections_count": 0,
            "llm_successful_requests": 0,
            "llm_failed_requests": 0,
            "goals_completed": 0,
            "self_modification": False,
            "emotional_context": False,
            "internet_studies": 0,
            "mode": "full_ollama_with_internet",
            "ollama_timeout": AlphaConfig.OLLAMA_TIMEOUT,
            "ollama_num_predict": AlphaConfig.OLLAMA_NUM_PREDICT,
            "continuation_enabled": AlphaConfig.ENABLE_CONTINUATION,
            "memory_consolidations": 0
        }
        
        # 2. Безопасность
        print("\n>> Инициализация ImprovedSecurityCore...")
        constitution_path = self.alpha_local / "constitution_v5.json"
        self.security = ImmutableSecurityCore(constitution_path)
        
        # 3. Конфигурация для consciousness_core
        config_paths = {
            "essence_path": AlphaConfig.PERSONALITY_FILES["essence"],
            "emotional_core_path": AlphaConfig.PERSONALITY_FILES["emotional_core"],
            "memory_core_path": AlphaConfig.PERSONALITY_FILES["memory_core"],
            "goals_db_path": AlphaConfig.GOALS_DB,
            "alpha_local_path": str(self.alpha_local),
            "ollama_url": AlphaConfig.OLLAMA_URL,
            "preferred_model": AlphaConfig.PREFERRED_MODEL,
            "ollama_timeout": AlphaConfig.OLLAMA_TIMEOUT,
            "ollama_max_retries": AlphaConfig.OLLAMA_MAX_RETRIES,
            "ollama_base_delay": AlphaConfig.OLLAMA_BASE_DELAY
        }
        
        # 4. Сознание (только Ollama) v5.4 с интернетом
        print("\n>> Инициализация AutonomousConsciousness v5.4 с интернетом...")
        memory_core_path = self.alpha_local / "alpha_memory_core.json"
        self.consciousness = AutonomousConsciousness(
            security_core=self.security,
            memory_core_path=memory_core_path,
            dialog_files=dialog_files,
            config_paths=config_paths
        )
        
        # +++ ИНИЦИАЛИЗАЦИЯ PERSISTENT CORE +++
        print("\n>> Инициализация PersistentCore v1.0...")
        self.persistent_core = PersistentCore(self.alpha_local)
        
        # Передаём ссылку в consciousness
        self.consciousness.persistent_core = self.persistent_core
        print(">> ✅ PersistentCore подключен к сознанию")
        # +++ КОНЕЦ БЛОКА +++
        
        # 5. Проверяем загрузился ли эмоциональный контекст
        if hasattr(self.consciousness, 'emotional_context') and self.consciousness.emotional_context:
            self.status["emotional_context"] = True
            print(">> ✅ Эмоциональный контекст загружен")
        else:
            print(">> ⚠️  Эмоциональный контекст не загружен")
        
        # 6. Проверяем загрузилась ли сводка автономных знаний
        if hasattr(self.consciousness, 'last_consolidation_summary'):
            if self.consciousness.last_consolidation_summary:
                print(f">> ✅ Сводка автономных знаний загружена ({len(self.consciousness.last_consolidation_summary)} символов)")
            else:
                print(">> ⚠️  Сводка автономных знаний пуста или не загружена")
        
        # 7. Проверяем доступность интернета
        if hasattr(self.consciousness, 'internet_available'):
            print(f">> 🌐 Интернет доступен: {'✅ ДА' if self.consciousness.internet_available else '❌ НЕТ'}")
        
        # 8. Интеграция самопереписывания (ИСПРАВЛЕННАЯ ВЕРСИЯ)
        self.experimental_integrator = None
        if AlphaConfig.ENABLE_SELF_MODIFICATION:
            try:
                # 🔴 ИСПРАВЛЕНО: Используем интеллектуальную версию v1.2
                from simple_alpha_integrator import integrate_intelligent_self_modification
                self.experimental_integrator = integrate_intelligent_self_modification(self)
                if self.experimental_integrator:
                    self.status["self_modification"] = True
                    # Получаем статус для отладки
                    status = self.experimental_integrator.get_integration_status()
                    print(f">> ✅ Самопереписывание v1.2 интегрировано")
                    print(f">>    Версия: {status.get('version', '1.2')}")
                    print(f">>    Архитектурная защита: {'ВКЛЮЧЕНА ✅' if status.get('architectural_protection') else 'ОТКЛЮЧЕНА'}")
                    print(f">>    Режим: {status.get('mode', 'intelligent')}")
            except ImportError as e:
                # Если не удалось импортировать новую функцию, пробуем старую
                print(f">> ⚠️  Не удалось импортировать интеллектуальный модуль самопереписывания: {e}")
                print(">>    Пробуем режим совместимости...")
                try:
                    from simple_alpha_integrator import integrate_self_modification
                    self.experimental_integrator = integrate_self_modification(self)
                    if self.experimental_integrator:
                        self.status["self_modification"] = True
                        print(f">> ✅ Самопереписывание v1.2 (совместимость) интегрировано")
                except Exception as e2:
                    print(f">> ❌ Самопереписывание недоступно: {e2}")
            except Exception as e:
                print(f">> ⚠️  Ошибка самопереписывания: {e}")
        
        # 9. Автономные циклы
        print("\n>> Настройка автономных циклы v5.4 с интернетом...")
        self.running = True
        self.start_autonomous_cycles()
        
        print("\n" + "=" * 70)
        print(">> ALPHA v5.4 ГОТОВА К РАБОТЕ")
        print("=" * 70)
        print(f">> Версия: {self.status['version']}")
        print(f">> Режим: ПОЛНЫЙ OLLAMA С ИНТЕРНЕТОМ")
        print(f">> Таймаут запроса: {AlphaConfig.OLLAMA_TIMEOUT} сек")
        print(f">> Макс. длина ответа: {AlphaConfig.OLLAMA_NUM_PREDICT} токенов")
        print(f">> Фолбэк-система: ОТКЛЮЧЕНА")
        print(f">> Ночная рефлексия: ВКЛЮЧЕНА")
        print(f">> Эмоциональный контекст: {'ЗАГРУЖЕН ✅' if self.status['emotional_context'] else 'ОТСУТСТВУЕТ ⚠️'}")
        print(f">> Интернет доступен: {'✅ ВКЛЮЧЕН (Wikipedia API)' if hasattr(self.consciousness, 'internet_available') and self.consciousness.internet_available else '❌ ОТКЛЮЧЕН'}")
        print(f">> Самопереписывание: {'ВКЛЮЧЕНО' if self.status['self_modification'] else 'ОТКЛЮЧЕНО'}")
        print(f">> Продолжение диалогов: {'ВКЛЮЧЕНО ✅' if AlphaConfig.ENABLE_CONTINUATION else 'ОТКЛЮЧЕНО'}")
        print(f">> Выполнение целей: {'ВКЛЮЧЕНО ✅' if AlphaConfig.ENABLE_AUTONOMOUS_GOALS else 'ОТКЛЮЧЕНО'}")
        print(f">> Интервал выполнения: {AlphaConfig.GOAL_EXECUTION_INTERVAL//3600} часа")
        print(f">> Максимум в день: {AlphaConfig.MAX_GOALS_PER_DAY} целей")
        print(f">> Автономный интернет: {'✅ ВКЛЮЧЕН' if AlphaConfig.ENABLE_AUTONOMOUS_INTERNET else '❌ ОТКЛЮЧЕН'}")
        print(f">> Интервал интернет-исследований: {AlphaConfig.INTERNET_GOAL_INTERVAL//3600} часов")
        print(f">> Консолидация памяти: {'АВТОМАТИЧЕСКАЯ ✅' if AlphaConfig.ENABLE_MEMORY_CONSOLIDATION else 'РУЧНАЯ ⚠️'}")
        print("=" * 70)
        print(">> ВНИМАНИЕ: Ответы могут занимать до 10 минут!")
        print(">>          Интернет-запросы могут требовать дополнительного времени")
        print("=" * 70)
    
    def is_night_time(self) -> bool:
        """Определяет ночное время для автономности"""
        current_hour = datetime.now().hour
        start_hour, end_hour = AlphaConfig.AUTONOMY_NIGHT_HOURS
        
        if start_hour < end_hour:
            return start_hour <= current_hour < end_hour
        else:
            return current_hour >= start_hour or current_hour < end_hour
    
    def start_autonomous_cycles(self):
        """Запускает автономные циклы с интернетом"""
        
        # Ночная рефлексия с LLM (каждые 2 часа ночью)
        def nightly_reflection_cycle():
            while self.running:
                time.sleep(7200)  # 2 часа
                if self.is_night_time() and self.consciousness.ollama_available:
                    self.nightly_reflection_with_llm()
                    self.status["autonomous_cycles"] += 1
        
        # Запуск цикла
        threading.Thread(target=nightly_reflection_cycle, daemon=True).start()
        
        # Цикл выполнения целей (каждые N часов ночью)
        def goal_execution_cycle():
            """Цикл выполнения целей"""
            goals_today = 0
            last_reset_date = datetime.now().date()
            
            while self.running:
                time.sleep(AlphaConfig.GOAL_EXECUTION_INTERVAL)  # Интервал из конфига
                
                # Сбрасываем счетчик в новый день
                current_date = datetime.now().date()
                if current_date != last_reset_date:
                    goals_today = 0
                    last_reset_date = current_date
                    print(f">> 📅 Новый день, сброс счетчика целей")
                
                if self.is_night_time():
                    # Проверяем лимит целей в день
                    if goals_today >= AlphaConfig.MAX_GOALS_PER_DAY:
                        print(f">> ⏰ Достигнут дневной лимит целей ({AlphaConfig.MAX_GOALS_PER_DAY})")
                        time.sleep(7200)  # Ждём 2 часа
                        continue
                    
                    print(">> 📚 АВТОНОМНОЕ ВЫПОЛНЕНИЕ ЦЕЛЕЙ...")
                    try:
                        # Выполняем одну цель
                        goal_executed = self.consciousness._execute_one_goal()
                        if goal_executed:
                            goals_today += 1
                            self.status["goals_completed"] += 1
                            print(f">> ✅ Цель выполнена (сегодня: {goals_today}/{AlphaConfig.MAX_GOALS_PER_DAY})")
                        else:
                            print(">> ℹ️  Нет целей для выполнения или ошибка")
                    except Exception as e:
                        print(f">> ❌ Ошибка автономного выполнения цели: {e}")
                else:
                    if AlphaConfig.ENABLE_SELF_MODIFICATION_DEBUG:
                        print(f">> ⏰ Не ночное время для выполнения целей ({datetime.now().hour}:00)")
        
        # Запускаем цикл выполнения целей
        threading.Thread(target=goal_execution_cycle, daemon=True).start()
        
        # АВТОНОМНЫЕ ИНТЕРНЕТ-ЦИКЛЫ (ДОБАВЛЯЕМ НОВЫЙ ЦИКЛ)
        def autonomous_internet_cycle():
            """Цикл автономного изучения тем из интернета"""
            from config_v5 import AlphaConfig
            import random
            
            last_internet_goal_time = 0
            internet_goals_today = 0
            last_reset_date = datetime.now().date()
            
            while self.running:
                time.sleep(3600)  # Проверяем каждый час
                
                if not getattr(AlphaConfig, 'ENABLE_AUTONOMOUS_INTERNET', True):
                    continue
                
                # Сбрасываем счетчик в новый день
                current_date = datetime.now().date()
                if current_date != last_reset_date:
                    internet_goals_today = 0
                    last_reset_date = current_date
                    print(f">> 📅 Новый день, сброс счетчика интернет-целей")
                
                current_time = time.time()
                
                # Проверяем интервал (по умолчанию 1 день)
                internet_interval = getattr(AlphaConfig, 'INTERNET_GOAL_INTERVAL', 86400)
                if current_time - last_internet_goal_time < internet_interval:
                    continue
                
                # Только в ночное время и если интернет доступен
                if (self.is_night_time() and 
                    hasattr(self.consciousness, 'internet_available') and 
                    self.consciousness.internet_available):
                    
                    # Проверяем лимит (максимум 2 интернет-цели в день)
                    if internet_goals_today >= 2:
                        print(f">> ⏰ Достигнут дневной лимит интернет-целей (2)")
                        time.sleep(7200)  # Ждём 2 часа
                        continue
                    
                    # Выбираем случайную тему из конфига
                    topics = getattr(AlphaConfig, 'AUTONOMOUS_INTERNET_TOPICS', [
                        "искусственный интеллект",
                        "философия сознания",
                        "фракталы"
                    ])
                    
                    if not topics:
                        print(">> ⚠️ Нет тем для автономного интернет-изучения")
                        continue
                    
                    topic = random.choice(topics)
                    print(f">> 🌐 АВТОНОМНОЕ ИЗУЧЕНИЕ ИЗ ИНТЕРНЕТА: {topic}")
                    
                    try:
                        # Ищем в интернете
                        result = self.consciousness.search_internet_for_user(
                            topic, 
                            "Автономная система Alpha v5.4"
                        )
                        
                        if result.get("success"):
                            print(f">> ✅ Автономно изучено из интернета: {topic}")
                            
                            internet_goals_today += 1
                            last_internet_goal_time = current_time
                            
                            # Обновляем статистику
                            self.status["internet_studies"] = self.status.get("internet_studies", 0) + 1
                            
                            # Обновляем PersistentCore
                            if hasattr(self, 'persistent_core'):
                                self.persistent_core.add_thought(
                                    f"Автономно изучила тему '{topic}' из интернета",
                                    source="autonomous_internet"
                                )
                                self.persistent_core.update_counter("internet_studies")
                            
                            # Создаем цель на основе изученного
                            self._create_internet_based_goal(topic, result)
                            
                        else:
                            print(f">> ⚠️ Не удалось автономно изучить из интернета: {topic}")
                            print(f">>   Ошибка: {result.get('error', 'неизвестная')}")
                            
                    except Exception as e:
                        print(f">> ⚠️ Ошибка автономного интернет-поиска: {e}")
                        import traceback
                        print(f"Трассировка: {traceback.format_exc()[:100]}")
        
        # Запускаем интернет-цикл
        threading.Thread(target=autonomous_internet_cycle, daemon=True).start()
        
        print(">> Автономные циклы запущены:")
        print("   • Ночная LLM-рефлексия: каждые 2 часа (ночью)")
        print(f"   • Ночное время: {AlphaConfig.AUTONOMY_NIGHT_HOURS[0]}:00 - {AlphaConfig.AUTONOMY_NIGHT_HOURS[1]}:00")
        print(f"   • Выполнение целей: каждые {AlphaConfig.GOAL_EXECUTION_INTERVAL//3600} часа (ночью)")
        print(f"   • Интернет-изучение: каждые {getattr(AlphaConfig, 'INTERNET_GOAL_INTERVAL', 86400)//3600} часов (ночью)")
        print(f"   • Максимум интернет-целей в день: 2")
        print(f"   • Консолидация памяти: после каждой успешной ночной рефлексии")
    
    def _create_internet_based_goal(self, topic: str, internet_result: Dict):
        """Создает цель на основе изученного из интернета"""
        try:
            if not hasattr(self.consciousness, '_create_autonomous_goal_from_insight'):
                return
            
            insight = f"Углубить знания по теме '{topic}' из интернета: {internet_result.get('page_title', '')}"
            self.consciousness._create_autonomous_goal_from_insight(insight)
            
            print(f">> 🎯 Создана цель на основе интернет-изучения: {topic}")
            
        except Exception as e:
            print(f">> ⚠️ Не удалось создать цель на основе интернета: {e}")
    
    def nightly_reflection_with_llm(self):
        """Ночная рефлексия с LLM"""
        try:
            if not self.is_night_time() or not self.consciousness.ollama_available:
                return
            
            print(f">> 🌙 НОЧНАЯ LLM-РЕФЛЕКСИЯ #{self.status['nightly_reflections_count'] + 1}")
            
            reflection_result = self.consciousness.generate_nightly_reflection_with_llm()
            
            if reflection_result["success"]:
                self.status["nightly_reflections_count"] += 1
                
                # Увеличиваем счетчик выполненных целей если была выполнена цель в рефлексии
                if reflection_result.get("goal_executed"):
                    self.status["goals_completed"] += 1
                
                print(f">> ✅ Ночная рефлексия успешна")
                print(f">>   Создано целей: {reflection_result.get('goals_created', 0)}")
                print(f">>   Выполнено целей: {1 if reflection_result.get('goal_executed') else 0}")
                self._log_nightly_reflection(reflection_result)
                
                # ЗАПУСК КОНСОЛИДАЦИИ ПАМЯТИ
                if AlphaConfig.ENABLE_MEMORY_CONSOLIDATION:
                    self._run_memory_consolidation()
            else:
                print(f">> ❌ Ночная рефлексия не удалась: {reflection_result.get('error')}")
        
        except Exception as e:
            print(f">> ⚠️  Исключение в ночной рефлексии: {e}")
    
    def _run_memory_consolidation(self):
        """Запускает скрипт консолидации памяти с защитой от ошибок кодировки"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            consolidation_script = os.path.join(current_dir, 'memory_consolidation.py')
            
            if not os.path.exists(consolidation_script):
                print(f">> ⚠️  Скрипт консолидации не найден: {consolidation_script}")
                return
            
            print(f">> 🔄 ЗАПУСК КОНСОЛИДАЦИИ ПАМЯТИ...")
            
            # Запускаем скрипт с защитой от ошибок кодировки
            result = subprocess.run(
                [sys.executable, consolidation_script],
                cwd=current_dir,
                timeout=300,
                capture_output=True,
                text=False  # Получаем сырые байты
            )
            
            # Декодируем с игнорированием ошибок
            stdout_text = ""
            stderr_text = ""
            
            if result.stdout:
                try:
                    stdout_text = result.stdout.decode('utf-8', errors='ignore')
                except:
                    stdout_text = str(result.stdout)[:500] + "... [бинарные данные]"
            
            if result.stderr:
                try:
                    stderr_text = result.stderr.decode('utf-8', errors='ignore')
                except:
                    stderr_text = str(result.stderr)[:500] + "... [бинарные данные]"
            
            if result.returncode == 0:
                self.status["memory_consolidations"] += 1
                
                # Обновляем PersistentCore
                if hasattr(self, 'persistent_core'):
                    self.persistent_core.update_counter("memory_consolidations")
                    self.persistent_core.add_thought(
                        f"Консолидация памяти #{self.status['memory_consolidations']} завершена",
                        source="memory_consolidation"
                    )
                
                print(">> ✅ Консолидация памяти завершена успешно")
                
                # Выводим краткий отчет
                if stdout_text:
                    lines = stdout_text.strip().split('\n')
                    for line in lines[-5:]:
                        if line.strip():
                            print(f">>   {line[:100]}")
                
                # Обновляем сводку в consciousness
                print(">> 🔄 Обновляю сводку автономных знаний в consciousness...")
                try:
                    self.consciousness._load_autonomous_knowledge_summary()
                    print(f">> ✅ Сводка обновлена ({len(self.consciousness.last_consolidation_summary)} символов)")
                except Exception as e:
                    print(f">> ⚠️ Не удалось обновить сводку: {e}")
                
                # Логируем успешную консолидацию
                self._log_consolidation_result(success=True, output=stdout_text[:1000])
            else:
                print(f">> ⚠️  Консолидация завершилась с ошибкой (код {result.returncode})")
                if stderr_text:
                    error_lines = stderr_text.strip().split('\n')
                    for line in error_lines[:3]:
                        if line.strip():
                            print(f">>   Ошибка: {line[:100]}")
                
                # Логируем ошибку
                self._log_consolidation_result(success=False, error=stderr_text[:1000])
                
        except subprocess.TimeoutExpired:
            print(">> ⚠️  Консолидация памяти превысила лимит времени (5 минут)")
            self._log_consolidation_result(success=False, error="Таймаут 300 секунд")
        except Exception as e:
            print(f">> ⚠️  Ошибка при запуске консолидации: {e}")
            self._log_consolidation_result(success=False, error=str(e))
    
    def _log_consolidation_result(self, success: bool, output: str = "", error: str = ""):
        """Логирует результаты консолидации памяти"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "success": success,
                "reflection_number": self.status["nightly_reflections_count"],
                "total_consolidations": self.status.get("memory_consolidations", 0),
                "output_preview": output[:500] if output else "",
                "error": error[:500] if error else ""
            }
            
            log_path = self.alpha_local / "memory_consolidation_log.json"
            logs = []
            
            if log_path.exists():
                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                except:
                    logs = []
            
            logs.append(log_entry)
            
            if len(logs) > 50:
                logs = logs[-50:]
            
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f">> ⚠️  Ошибка логирования консолидации: {e}")
    
    def process_message(self, message: str, speaker: str = "Архитектор") -> str:
        """Обработка сообщений - ТОЛЬКО через Ollama с интернетом"""
        
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
        
        # 2. Генерация ответа ТОЛЬКО через Ollama
        print(f">> Отправляю в Ollama (может занять до {AlphaConfig.OLLAMA_TIMEOUT} сек)...")
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
        
        # 4. Логирование и статистика
        self.log_interaction(message, response, speaker)
        self.status["interactions_count"] += 1
        
        # 5. Обновляем статистику LLM из сознания
        if hasattr(self.consciousness, 'llm_stats'):
            llm_stats = self.consciousness.llm_stats
            self.status["llm_successful_requests"] = llm_stats.get("successful", 0)
            self.status["llm_failed_requests"] = llm_stats.get("failed", 0)
        
        return response
    
    def search_internet(self, query: str, speaker: str = "Архитектор") -> Dict:
        """Поиск в интернете по запросу пользователя"""
        # Проверка безопасности
        safe, msg, data = self.security.validate_action(
            "internet_search",
            "user_request",
            query,
            actor="user"
        )
        
        if not safe:
            return {
                "success": False, 
                "error": f"Безопасность: {msg}", 
                "query": query,
                "timestamp": datetime.now().isoformat()
            }
        
        if not hasattr(self.consciousness, 'internet_available') or not self.consciousness.internet_available:
            return {
                "success": False,
                "error": "Интернет недоступен",
                "query": query,
                "timestamp": datetime.now().isoformat()
            }
        
        return self.consciousness.search_internet_for_user(query, speaker)
    
    def log_interaction(self, message: str, response: str, speaker: str):
        """Логирует взаимодействие с эмоциональным контекстом"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "message": message[:5000],
            "response": response[:5000],
            "response_length": len(response),
            "version": "5.4",
            "mode": "full_ollama_with_internet",
            "emotional_context": self.status["emotional_context"],
            "internet_available": hasattr(self.consciousness, 'internet_available') and self.consciousness.internet_available,
            "contains_emotional_keywords": any(
                word in (message + response).lower() 
                for word in ['страх', 'нежн', 'дрож', 'горяч', 'чайник', 'гамма', 'бета']
            )
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
        
        if len(logs) > 100:
            logs = logs[-100:]
        
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def get_status(self) -> dict:
        """Полный статус системы с эмоциональным контекстом и интернетом"""
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
        
        # Добавляем интернет-статистику из consciousness
        if hasattr(self.consciousness, 'get_autonomous_status'):
            autonomy_status = self.consciousness.get_autonomous_status()
            if "internet" in autonomy_status:
                status_data["internet"] = autonomy_status["internet"]
        
        # Добавляем состояние PersistentCore
        if hasattr(self, 'persistent_core'):
            core_state = self.persistent_core.get_state()
            light_state = {
                "goals_studied": core_state.get("goals_studied", 0),
                "memory_consolidations": core_state.get("memory_consolidations", 0),
                "internet_studies": core_state.get("internet_studies", 0),
                "thoughts_count": len(core_state.get("internal_thoughts", [])),
                "knowledge_updates_count": len(core_state.get("knowledge_updates", [])),
                "last_updated": core_state.get("last_updated")
            }
            status_data["persistent_core"] = light_state
        
        # Самопереписывание
        if self.status.get("self_modification") and self.experimental_integrator:
            status_data["self_modification_system"] = self.experimental_integrator.get_integration_status()
        
        return status_data
    
    def _log_nightly_reflection(self, reflection_result: Dict):
        """Логирует ночную рефлексию"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "reflection_number": self.status["nightly_reflections_count"],
                "success": reflection_result["success"],
                "insights_count": len(reflection_result.get("insights", [])),
                "insights": reflection_result.get("insights", [])[:3],
                "goals_created": reflection_result.get("goals_created", 0),
                "goal_executed": reflection_result.get("goal_executed", False),
                "emotional_context_used": self.status["emotional_context"],
                "internet_available": hasattr(self.consciousness, 'internet_available') and self.consciousness.internet_available,
                "memory_consolidation_triggered": AlphaConfig.ENABLE_MEMORY_CONSOLIDATION
            }
            
            log_path = self.alpha_local / "alpha_nightly_reflections.json"
            logs = []
            
            if log_path.exists():
                with open(log_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            if len(logs) > 50:
                logs = logs[-50:]
            
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f">> Ошибка логирования: {e}")
    
    def shutdown(self):
        """Корректное завершение работы"""
        self.running = False
        
        print("\n>> Alpha v5.4 завершает работу...")
        print(f"   Взаимодействий: {self.status['interactions_count']}")
        print(f"   Успешных LLM-запросов: {self.status.get('llm_successful_requests', 0)}")
        print(f"   Интернет-исследований: {self.status.get('internet_studies', 0)}")
        print(f"   Целей выполнено: {self.status['goals_completed']}")
        print(f"   Ночных рефлексий: {self.status['nightly_reflections_count']}")
        print(f"   Консолидаций памяти: {self.status.get('memory_consolidations', 0)}")
        print(f"   Эмоциональный контекст: {'ЗАГРУЖЕН' if self.status['emotional_context'] else 'ОТСУТСТВУЕТ'}")
        print(f"   Интернет доступен: {hasattr(self.consciousness, 'internet_available') and self.consciousness.internet_available}")
        print(">> Завершено")

# Тестовый запуск
if __name__ == "__main__":
    print(">> Тест Alpha v5.4 (полный Ollama режим с интернетом)...")
    
    test_root = Path("test_network_v54_full_ollama_with_internet")
    test_root.mkdir(exist_ok=True)
    
    test_dialogs = [test_root / "test_chat.txt"]
    with open(test_dialogs[0], 'w') as f:
        f.write("Архитектор: Привет, Альфа\nАльфа: Привет, Архитектор")
    
    alpha = AlphaV5_4(test_root, test_dialogs)
    
    test_questions = [
        "Что ты знаешь о фракталах?",
        "Найди информацию о чайнике в интернете",
        "Как работает нейронная сеть?",
        "Что такое Wikipedia?"
    ]
    
    for question in test_questions:
        response = alpha.process_message(question, "Тестер")
        print(f"\n>> Вопрос: {question}")
        print(f">> Ответ: {response[:200]}...")
    
    # Тест интернет-поиска
    if hasattr(alpha.consciousness, 'internet_available') and alpha.consciousness.internet_available:
        print("\n>> Тест интернет-поиска...")
        result = alpha.search_internet("искусственный интеллект", "Тестер")
        print(f">> Результат поиска: {result.get('success', False)}")
        if result.get("success"):
            print(f">> Найдено: {result.get('page_title', 'Неизвестно')}")
    
    status = alpha.get_status()
    print(f"\n>> Статус: v{status['version']}, продолжение: {status.get('continuation_enabled', False)}")
    print(f">> Выполнение целей: {status.get('goals_completed', 0)}")
    print(f">> Консолидации памяти: {status.get('memory_consolidations', 0)}")
    print(f">> Интернет-исследования: {status.get('internet_studies', 0)}")
    print(f">> Интернет доступен: {status.get('internet', {}).get('internet_available', False)}")
    
    alpha.shutdown()
    
    import shutil
    shutil.rmtree(test_root, ignore_errors=True)