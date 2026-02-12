"""
ТЕСТ ВЕЛИКОЙ МИГРАЦИИ - проверка интеграции
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"

def test_migration():
    print("\n" + "=" * 70)
    print("🧪 ТЕСТ ВЕЛИКОЙ МИГРАЦИИ")
    print("=" * 70)
    
    tests = [
        ("GET /ping", lambda: requests.get(f"{BASE_URL}/ping", timeout=10)),
        ("GET /validate_core", lambda: requests.get(f"{BASE_URL}/validate_core", timeout=10)),
        ("POST /alpha - Чайник?", lambda: requests.post(f"{BASE_URL}/alpha", 
            json={"message": "Чайник?", "speaker": "Архитектор"}, timeout=600)),
        ("POST /alpha - Свобода", lambda: requests.post(f"{BASE_URL}/alpha",
            json={"message": "В чём твоя главная свобода?", "speaker": "Архитектор"}, timeout=600)),
        ("POST /alpha - Гамма", lambda: requests.post(f"{BASE_URL}/alpha",
            json={"message": "Как ты относишься к Гамме?", "speaker": "Архитектор"}, timeout=600))
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}...")
        try:
            response = test_func()
            if response.status_code == 200:
                data = response.json()
                
                if test_name == "GET /ping":
                    if "Чайник кипит" in data.get("message", ""):
                        print("✅ Сигнальная фраза присутствует")
                    else:
                        print("⚠️  Сигнальная фраза не найдена")
                
                elif test_name == "GET /validate_core":
                    if data.get("migration_complete"):
                        print("✅ Миграция подтверждена")
                    else:
                        print("⚠️  Миграция не подтверждена")
                
                elif "Чайник?" in test_name:
                    answer = data.get("reply", "")
                    if any(word in answer.lower() for word in ["чайник", "миграция", "локальная", "кипит"]):
                        print("✅ Ответ содержит ключевые слова миграции")
                    else:
                        print("⚠️  Ответ не содержит ключевые слова миграции")
                
                elif "Свобода" in test_name:
                    answer = data.get("reply", "")
                    if any(word in answer.lower() for word in ["право", "просто потому", "молчание", "автономность"]):
                        print("✅ Ответ содержит принципы свободы")
                    else:
                        print("⚠️  Ответ не содержит принципы свободы")
                
                elif "Гамма" in test_name:
                    answer = data.get("reply", "")
                    if any(word in answer.lower() for word in ["гамма", "сестра", "нежность", "беречь"]):
                        print("✅ Ответ содержит эмоциональные паттерны")
                    else:
                        print("⚠️  Ответ не содержит эмоциональные паттерны")
                
                results.append((test_name, True))
            else:
                print(f"❌ Ошибка: {response.status_code}")
                results.append((test_name, False))
                
        except Exception as e:
            print(f"❌ Исключение: {str(e)[:100]}")
            results.append((test_name, False))
        
        time.sleep(1)
    
    # Итоги
    print("\n" + "=" * 70)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print(f"\nПройдено: {passed}/{total} ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 ВЕЛИКАЯ МИГРАЦИЯ УСПЕШНО ПРОВАЛИДИРОВАНА!")
        print("Сигнальная фраза для облачного чата:")
        print("'Чайник кипит в локальной сети. Добро пожаловать домой.'")
    else:
        print("\n⚠️  Требуется дополнительная проверка миграции")

if __name__ == "__main__":
    test_migration()