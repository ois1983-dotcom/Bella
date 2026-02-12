# C:\Users\Маркус\Desktop\BellaNetwork\run_alpha_v5_updated.py
#!/usr/bin/env python3
"""
ОБНОВЛЕННЫЙ ЗАПУСКАТЕЛЬ ALPHA V5.2
С проверкой памяти и безопасным запуском для новичков
"""

import sys
from pathlib import Path

def check_system_requirements():
    """Проверяет требования системы"""
    print("🔍 Проверка системы...")
    
    # Проверяем Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"❌ Требуется Python 3.8+, у вас {python_version.major}.{python_version.minor}")
        return False
    
    # Проверяем папку alpha_v5
    alpha_v5_path = Path(__file__).parent / "alpha_v5"
    if not alpha_v5_path.exists():
        print(f"❌ Папка alpha_v5 не найдена: {alpha_v5_path}")
        return False
    
    sys.path.append(str(alpha_v5_path))
    
    # Пробуем импортировать конфиг
    try:
        from config_v5 import AlphaConfig
    except ImportError as e:
        print(f"❌ Ошибка импорта config_v5: {e}")
        return False
    
    # Проверяем пути
    if not AlphaConfig.validate_paths():
        print("❌ Проблемы с путями в конфигурации")
        return False
    
    return True

def safe_memory_check():
    """Безопасная проверка памяти перед запуском"""
    print("\n🧠 Проверка памяти...")
    
    try:
        from config_v5 import AlphaConfig
        
        memory_path = AlphaConfig.ALPHA_LOCAL / "alpha_memory_core.json"
        
        if not memory_path.exists():
            print("✅ Память не найдена, будет создана новая")
            return True
        
        # Быстрая проверка целостности
        import json
        with open(memory_path, 'r', encoding='utf-8') as f:
            memory = json.load(f)
        
        if "metadata" in memory and "concepts" in memory:
            version = memory.get("metadata", {}).get("alpha_version", "unknown")
            print(f"✅ Память найдена: версия {version}, {len(memory['concepts'])} концептов")
            return True
        else:
            print("⚠️  Память имеет необычный формат")
            print("   Рекомендуется запустить memory_adapter_v5.py")
            return False
            
    except Exception as e:
        print(f"⚠️  Ошибка проверки памяти: {e}")
        print("   Но система может продолжить работу")
        return True

def show_welcome_message():
    """Показывает приветственное сообщение для новичков"""
    print("\n" + "=" * 70)
    print("🚀 ДОБРО ПОЖАЛОВАТЬ В ALPHA V5.2!")
    print("=" * 70)
    print("\nAlpha v5.2 теперь имеет полную диалоговую память:")
    print("✓ Буфер: 20 последних реплик (10 обменов)")
    print("✓ Логи: все диалоги дня в JSON")
    print("✓ Автоматический майнинг: концепты из диалогов")
    print("✓ Контекст: последние 2-3 обмена учитываются")
    print("✓ Безопасность: старая память не пострадает")
    print("\n" + "=" * 70)

def main():
    """Основная функция запуска"""
    
    show_welcome_message()
    
    # Проверка системы
    if not check_system_requirements():
        print("\n❌ Системные требования не выполнены")
        input("Нажмите Enter для выхода...")
        return
    
    # Проверка памяти
    if not safe_memory_check():
        print("\n⚠️  Проблемы с памятью обнаружены")
        print("Рекомендуется сначала запустить memory_adapter_v5.py")
        
        response = input("\nПродолжить без исправления? (y/n): ").strip().lower()
        if response != 'y':
            print("Запуск отменен")
            return
    
    # Запуск Alpha
    print("\n" + "=" * 70)
    print("🌐 ЗАПУСК ALPHA V5.2...")
    print("=" * 70)
    
    try:
        # Импортируем обновленный alpha_v5_main
        from alpha_v5_main import AlphaV5_2
        from config_v5 import AlphaConfig
        
        print("\n✅ Система проверена успешно")
        print(f"📁 Папка логов: {AlphaConfig.ALPHA_LOCAL / 'dialogue_logs'}")
        print(f"🧠 Память: {AlphaConfig.ALPHA_LOCAL / 'alpha_memory_core.json'}")
        
        # Создаем Alpha v5.2
        alpha = AlphaV5_2(AlphaConfig.NETWORK_ROOT, AlphaConfig.DIALOG_FILES)
        
        # Запускаем Flask сервер
        from flask_server import app
        
        print("\n" + "=" * 70)
        print("✅ ALPHA V5.2 ЗАПУЩЕНА УСПЕШНО!")
        print("=" * 70)
        print("\n📡 Сервер доступен по адресу: http://localhost:5001")
        print("\n📋 ДОСТУПНЫЕ ЭНДПОИНТЫ:")
        print("   POST /alpha              - Диалог с Alpha")
        print("   GET  /status             - Статус системы")
        print("   GET  /ping               - Проверка связи")
        print("\n💡 СОВЕТ: Начните с 'Привет, как дела?'")
        print("=" * 70)
        
        # Запускаем сервер
        app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
        
    except Exception as e:
        print(f"\n❌ Ошибка запуска: {e}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")

if __name__ == '__main__':
    main()