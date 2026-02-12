# C:\Users\Маркус\Desktop\BellaNetwork\run_alpha_v5.py
#!/usr/bin/env python3
"""
Простой запуск Alpha v5.0 с исправленным импортом
"""

import sys
from pathlib import Path

def main():
    print("=" * 70)
    print("🚀 ЗАПУСК ALPHA v5.0 - ПРОСТОЙ ИСПРАВЛЕННЫЙ ВАРИАНТ")
    print("=" * 70)
    
    # Добавляем путь к alpha_v5
    alpha_v5_path = Path(__file__).parent / "alpha_v5"
    if not alpha_v5_path.exists():
        print(f"❌ Папка alpha_v5 не найдена: {alpha_v5_path}")
        return
    
    sys.path.append(str(alpha_v5_path))
    
    # Проверяем конфигурацию
    try:
        from config_v5 import AlphaConfig
        
        print("\n🔍 Проверка путей...")
        if AlphaConfig.validate_paths():
            print("✅ Пути проверены")
        else:
            print("⚠️  Есть проблемы с путями, но продолжаем...")
        
    except Exception as e:
        print(f"⚠️  Ошибка конфигурации: {e}")
        print("Продолжаем...")
    
    # Запускаем Flask сервер
    print("\n" + "=" * 70)
    print("🌐 ЗАПУСК FLASK СЕРВЕРА...")
    print("=" * 70)
    
    try:
        # Импортируем напрямую
        from alpha_v5.flask_server import app
        
        print("Alpha v5.0 запущена и готова к работе!")
        print("\nСервер запущен на http://localhost:5001")
        print("Для проверки отправьте запрос:")
        print('curl http://localhost:5001/ping')
        print("\nИли запустите мессенджер:")
        print('python alpha_messenger_simple.py')
        print("=" * 70)
        
        app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
        
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()