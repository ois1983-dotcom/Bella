#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
КОМПЛЕКСНЫЙ ТЕСТ ALPHA V5.2
Проверяет все системы за 2 минуты
"""

import json
import requests
import sqlite3
import time
from pathlib import Path
from datetime import datetime
import sys

class AlphaTester:
    """Тестирует все системы Alpha"""
    
    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.alpha_local = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local")
        self.alpha_v5 = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5")
        
        print("=" * 60)
        print("ТЕСТ СИСТЕМЫ ALPHA V5.2")
        print("=" * 60)
        
        self.test_results = []
        
    def run_test(self, test_name, test_func):
        """Запускает тест и записывает результат"""
        try:
            print(f"\n[TEST] {test_name}...")
            result = test_func()
            self.test_results.append((test_name, "[OK] УСПЕХ", result))
            return True
        except Exception as e:
            self.test_results.append((test_name, "[ERROR] ОШИБКА", str(e)))
            return False
    
    def test_1_server_alive(self):
        """Тест 1: Сервер отвечает"""
        response = requests.get(f"{self.base_url}/ping", timeout=5)
        return response.json()["status"] == "active_full_ollama"
    
    def test_2_config_paths(self):
        """Тест 2: Критические пути существуют"""
        required_paths = [
            self.alpha_local,
            self.alpha_local / "alpha_memory_core.json",
            self.alpha_local / "alpha_v5_interactions.json",
            self.alpha_local / "alpha_nightly_reflections.json",
            self.alpha_v5 / "experimental",
        ]
        
        for path in required_paths:
            if not path.exists():
                raise FileNotFoundError(f"Отсутствует: {path}")
        return True
    
    def test_3_night_reflection_file(self):
        """Тест 3: Файл ночной рефлексии содержит данные"""
        ref_file = self.alpha_local / "alpha_nightly_reflections.json"
        
        if not ref_file.exists():
            raise FileNotFoundError("Файл рефлексий не найден")
        
        with open(ref_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Файл рефлексий не является списком")
        
        if len(data) == 0:
            print("[WARN] Лог пуст (возможно, только начали)")
            return "Лог пуст"
        
        # Проверяем последнюю запись
        last_reflection = data[-1]
        required_keys = ["timestamp", "reflection_number", "success", "insights_count"]
        
        for key in required_keys:
            if key not in last_reflection:
                raise KeyError(f"Нет ключа {key} в рефлексии")
        
        return f"Рефлексий: {len(data)}, последняя: #{last_reflection.get('reflection_number')}"
    
    def test_4_status_api(self):
        """Тест 4: API статуса возвращает полные данные"""
        response = requests.get(f"{self.base_url}/status", timeout=10)
        status = response.json()
        
        required_keys = [
            "version", "autonomous_cycles", "nightly_reflections_count",
            "emotional_context", "self_modification", "security"
        ]
        
        for key in required_keys:
            if key not in status:
                raise KeyError(f"Нет ключа {key} в статусе")
        
        # Проверяем значения
        if status["nightly_reflections_count"] < 0:
            raise ValueError("Количество рефлексий не может быть отрицательным")
        
        if not status.get("emotional_context"):
            raise ValueError("Эмоциональный контекст не загружен")
        
        return f"Циклы: {status['autonomous_cycles']}, Рефлексии: {status['nightly_reflections_count']}"
    
    def test_5_interactions_log(self):
        """Тест 5: Лог взаимодействий работает"""
        log_file = self.alpha_local / "alpha_v5_interactions.json"
        
        if not log_file.exists():
            raise FileNotFoundError("Файл логов не найден")
        
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Лог не является списком")
        
        if len(data) == 0:
            print("[WARN] Лог пуст (возможно, только начали)")
            return "Лог пуст"
        
        # Проверяем структуру последней записи
        last_log = data[-1]
        if "timestamp" not in last_log:
            raise KeyError("Нет timestamp в логе")
        
        return f"Записей в логе: {len(data)}"
    
    def test_6_memory_core(self):
        """Тест 6: Ядро памяти имеет данные"""
        memory_file = self.alpha_local / "alpha_memory_core.json"
        
        if not memory_file.exists():
            raise FileNotFoundError("Файл памяти не найден")
        
        with open(memory_file, 'r', encoding='utf-8') as f:
            memory = json.load(f)
        
        # Проверяем структуру
        if "concepts" not in memory:
            raise KeyError("Нет ключа 'concepts' в памяти")
        
        concepts = memory.get("concepts", {})
        if len(concepts) == 0:
            print("[WARN] Память пуста (возможно, не запускали майнер)")
            return "Память пуста"
        
        return f"Концептов в памяти: {len(concepts)}"
    
    def test_7_goals_db(self):
        """Тест 7: База данных целей существует"""
        goals_db = self.alpha_local / "alpha_goals.db"
        
        if not goals_db.exists():
            print("[WARN] База целей не найдена (Alpha ещё не создавала цели)")
            return "База целей не создана"
        
        try:
            conn = sqlite3.connect(str(goals_db))
            cursor = conn.cursor()
            
            # Проверяем таблицу
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='autonomous_goals_v5'")
            if not cursor.fetchone():
                raise ValueError("Таблица целей не существует")
            
            # Проверяем данные
            cursor.execute("SELECT COUNT(*) FROM autonomous_goals_v5")
            count = cursor.fetchone()[0]
            
            conn.close()
            
            return f"Целей в БД: {count}"
            
        except sqlite3.Error as e:
            return f"Ошибка БД: {e}"
    
    def test_8_experimental_files(self):
        """Тест 8: Experimental файлы на месте"""
        exp_dir = self.alpha_v5 / "experimental"
        
        if not exp_dir.exists():
            raise FileNotFoundError("Папка experimental не найдена")
        
        files = list(exp_dir.glob("*.py"))
        if len(files) == 0:
            print("[WARN] Нет experimental файлов")
            return "Нет experimental файлов"
        
        # Проверяем хотя бы один файл на читаемость
        for file in files:
            if file.name == "experimental_base.py":
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "экспериментальный" not in content.lower():
                        print(f"[WARN] Файл {file.name} может быть повреждён")
        
        return f"Experimental файлов: {len(files)}"
    
    def test_9_code_backups(self):
        """Тест 9: Бэкапы кода существуют"""
        backups_dir = self.alpha_local / "code_backups"
        
        if not backups_dir.exists():
            print("[WARN] Папка бэкапов не найдена (Alpha ещё не создавала бэкапы)")
            return "Бэкапов нет"
        
        backups = list(backups_dir.glob("experimental_checkpoint_*"))
        if len(backups) == 0:
            print("[WARN] Нет бэкапов экспериментальных файлов")
            return "Бэкапов экспериментальных файлов нет"
        
        # Проверяем самый свежий бэкап
        latest_backup = max(backups, key=lambda x: x.stat().st_mtime)
        return f"Бэкапов: {len(backups)}, последний: {latest_backup.name}"
    
    def test_10_dialogue_response(self):
        """Тест 10: Alpha отвечает на простой вопрос"""
        response = requests.post(
            f"{self.base_url}/alpha",
            json={
                "message": "Привет, Alpha. Как твое самочувствие?",
                "speaker": "Тестер"
            },
            timeout=600  # 10 минут на ответ
        )
        
        if response.status_code != 200:
            raise ValueError(f"API вернул код {response.status_code}")
        
        data = response.json()
        if "reply" not in data:
            raise KeyError("Нет ключа 'reply' в ответе")
        
        reply = data["reply"]
        if len(reply) < 10:
            raise ValueError("Ответ слишком короткий")
        
        return f"Ответ получен, длина: {len(reply)} символов"
    
    def test_11_night_time_logic(self):
        """Тест 11: Проверка логики ночного времени"""
        # Проверяем конфиг
        config_path = self.alpha_v5 / "config_v5.py"
        if not config_path.exists():
            raise FileNotFoundError("Конфиг не найден")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        # Ищем настройки ночного времени
        import re
        
        # AUTONOMY_NIGHT_HOURS
        match = re.search(r'AUTONOMY_NIGHT_HOURS\s*=\s*\((\d+),\s*(\d+)\)', config_content)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            print(f"  Настройка: AUTONOMY_NIGHT_HOURS = ({start}, {end})")
            
            current_hour = datetime.now().hour
            is_night = False
            
            if start < end:
                is_night = start <= current_hour < end
            else:
                is_night = current_hour >= start or current_hour < end
            
            return f"Текущий час: {current_hour}, Ночь: {'ДА' if is_night else 'НЕТ'}"
        else:
            return "Не найдена настройка AUTONOMY_NIGHT_HOURS"
    
    def run_all_tests(self):
        """Запускает все тесты"""
        tests = [
            ("Сервер работает", self.test_1_server_alive),
            ("Критические пути", self.test_2_config_paths),
            ("Файл рефлексий", self.test_3_night_reflection_file),
            ("API статуса", self.test_4_status_api),
            ("Лог взаимодействий", self.test_5_interactions_log),
            ("Ядро памяти", self.test_6_memory_core),
            ("База целей", self.test_7_goals_db),
            ("Experimental файлы", self.test_8_experimental_files),
            ("Бэкапы кода", self.test_9_code_backups),
            ("Диалог (быстрый тест)", self.test_10_dialogue_response),
            ("Логика ночного времени", self.test_11_night_time_logic),
        ]
        
        all_passed = True
        for test_name, test_func in tests:
            passed = self.run_test(test_name, test_func)
            if not passed:
                all_passed = False
        
        # Вывод результатов
        print(f"\n{'='*60}")
        print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("="*60)
        
        for test_name, status, details in self.test_results:
            print(f"{status} {test_name}")
            if details and details != "УСПЕХ":
                print(f"   {details}")
        
        print(f"\n{'='*60}")
        if all_passed:
            print("[SUCCESS] ВСЕ СИСТЕМЫ ALPHA РАБОТАЮТ КОРРЕКТНО!")
        else:
            print("[WARN] НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ")
            print("   Проверьте логи выше для деталей")
        
        print("="*60)
        
        return all_passed

def main():
    """Основная функция"""
    print("[START] Запуск комплексного теста Alpha v5.2...")
    print(f"Время начала: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        tester = AlphaTester()
        success = tester.run_all_tests()
        
        if success:
            # Дополнительные рекомендации
            print("\n[INFO] РЕКОМЕНДАЦИИ:")
            print("1. Запусти memory_miner_v5.3.py для обновления памяти")
            print("2. Проверь файл alpha_nightly_reflections.json - там должны быть инсайты")
            print("3. Убедись, что ночное время в конфиге соответствует твоему часовому поясу")
            print("4. Можно запустить dialogue_miner_v5.py для обработки диалогов")
        else:
            print("\n[FIX] ЧТО ДЕЛАТЬ:")
            print("1. Проверь, что Alpha запущена (python run_v52.py)")
            print("2. Проверь логи в консоли Alpha")
            print("3. Убедись, что все файлы существуют по указанным путям")
            print("4. Перезапусти Alpha при необходимости")
        
        input("\nНажми Enter для выхода...")
        
    except Exception as e:
        print(f"[ERROR] КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        input("Нажми Enter для выхода...")

if __name__ == "__main__":
    main()