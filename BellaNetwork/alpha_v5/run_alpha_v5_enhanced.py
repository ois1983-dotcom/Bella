# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\run_alpha_v5_enhanced.py
"""
СКРИПТ ЗАПУСКА ALPHA V5.4 С УЛУЧШЕННОЙ ПАМЯТЬЮ
"""

import sys
from pathlib import Path
import subprocess
import time
from datetime import datetime

def check_prerequisites():
    """Проверяет необходимые условия"""
    print("=" * 70)
    print("🔍 ПРОВЕРКА ПРЕДВАРИТЕЛЬНЫХ УСЛОВИЙ")
    print("=" * 70)
    
    # Проверяем Python
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        print("❌ Требуется Python 3.10 или выше")
        return False
    
    # Проверяем Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama доступен")
        else:
            print("❌ Ollama не отвечает")
            return False
    except:
        print("❌ Не удалось подключиться к Ollama")
        print("   Запустите Ollama: ollama serve")
        return False
    
    # Проверяем необходимые модули
    required_modules = [
        "flask",
        "requests", 
        "sqlite3",
        "json",
        "pathlib"
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ Модуль {module} доступен")
        except ImportError:
            print(f"❌ Модуль {module} не найден")
            return False
    
    return True

def run_memory_migration():
    """Запускает миграцию памяти"""
    print("\n" + "=" * 70)
    print("🧠 ЗАПУСК МИГРАЦИИ ПАМЯТИ V5.4")
    print("=" * 70)
    
    try:
        from memory_adapter_v5_enhanced import EnhancedMemoryAdapter
        from config_v5 import AlphaConfig
        
        adapter = EnhancedMemoryAdapter(AlphaConfig.ALPHA_LOCAL)
        adapter.run_full_migration()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка миграции памяти: {e}")
        print("⚠️  Продолжаем с существующей памятью")
        return False

def run_enhanced_memory_miner():
    """Запускает улучшенный майнер памяти"""
    print("\n" + "=" * 70)
    print("🕵️  ЗАПУСК УЛУЧШЕННОГО МАЙНЕРА ПАМЯТИ")
    print("=" * 70)
    
    try:
        # Проверяем, нужно ли запускать майнер
        from config_v5 import AlphaConfig
        
        memory_path = AlphaConfig.ALPHA_LOCAL / "alpha_memory_core.json"
        if memory_path.exists():
            # Проверяем возраст файла
            file_age = time.time() - memory_path.stat().st_mtime
            if file_age < 86400:  # 24 часа
                print("✅ Память актуальна (менее 24 часов)")
                return True
        
        from memory_miner_v5_4 import EnhancedMemoryMiner
        miner = EnhancedMemoryMiner()
        miner.run()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка майнера памяти: {e}")
        print("⚠️  Продолжаем с существующей памятью")
        return False

def start_alpha_server():
    """Запускает сервер Alpha"""
    print("\n" + "=" * 70)
    print("🚀 ЗАПУСК ALPHA V5.4 СЕРВЕРА")
    print("=" * 70)
    
    try:
        from flask_server import app
        
        # Проверяем конфигурацию
        from config_v5 import AlphaConfig
        if not AlphaConfig.validate_paths():
            print("❌ Проблемы с путями конфигурации")
            return False
        
        print("✅ Конфигурация проверена")
        print(f"   Модель: {AlphaConfig.PREFERRED_MODEL}")
        print(f"   Таймаут: {AlphaConfig.OLLAMA_TIMEOUT} сек")
        print(f"   Длина ответа: до {AlphaConfig.OLLAMA_NUM_PREDICT} токенов")
        
        print("\n" + "=" * 70)
        print("🌐 СЕРВЕР ЗАПУЩЕН НА http://localhost:5001")
        print("=" * 70)
        print("\nЭНДПОИНТЫ:")
        print("  POST /alpha    - Основной диалог")
        print("  GET  /status   - Статус системы")
        print("  GET  /ping     - Проверка связи")
        print("\n📝 ЛОГИ:")
        print("  • alpha_v5_interactions.json - История диалогов")
        print("  • alpha_server.log - Логи сервера")
        print("  • dialogue_summary.txt - Анализ диалогов")
        print("\n⚡ ОСОБЕННОСТИ V5.4:")
        print("  1. Улучшенное продолжение диалогов")
        print("  2. Увеличенная длина ответов (1500 токенов)")
        print("  3. Интегрированная память с диалогами")
        print("  4. Автоматическое завершение мыслей")
        print("=" * 70)
        
        # Запускаем сервер
        app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        return False

def create_startup_log():
    """Создает лог запуска"""
    log_path = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local") / "startup_log.txt"
    
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Запуск Alpha v5.4 - {datetime.now().isoformat()}\n")
        f.write(f"{'='*60}\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Платформа: {sys.platform}\n")

def main():
    """Основная функция запуска"""
    create_startup_log()
    
    print("\n" + "=" * 70)
    print("🚀 ЗАПУСК ALPHA V5.4 - УЛУЧШЕННАЯ ВЕРСИЯ")
    print("=" * 70)
    
    # 1. Проверка условий
    if not check_prerequisites():
        print("\n❌ Не выполнены предварительные условия")
        return
    
    # 2. Миграция памяти (если нужно)
    run_memory_migration()
    
    # 3. Запуск майнера памяти (если нужно)
    run_enhanced_memory_miner()
    
    # 4. Запуск сервера
    print("\n▶️  Запускаю Alpha v5.4 сервер...")
    start_alpha_server()

if __name__ == "__main__":
    main()