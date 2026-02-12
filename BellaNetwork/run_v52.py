# C:\Users\Маркус\Desktop\BellaNetwork\run_v52.py
#!/usr/bin/env python3
"""
ПРОСТОЙ ЗАПУСКАТЕЛЬ ALPHA V5.2 С УМНЫМ СЖАТИЕМ
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "alpha_v5"))

try:
    from alpha_v5_main import AlphaV5_2
    from config_v5 import AlphaConfig
    from flask_server import app
    
    print("=" * 70)
    print("🚀 ЗАПУСК ALPHA V5.2 (УМНОЕ СЖАТИЕ КОНТЕКСТА)")
    print("=" * 70)
    
    # Создаем Alpha
    alpha = AlphaV5_2(AlphaConfig.NETWORK_ROOT, AlphaConfig.DIALOG_FILES)
    
    print("\n✅ Alpha v5.2 запущена!")
    print(f"📡 Сервер доступен по адресу: http://localhost:5001")
    print(f"📊 Уровень сжатия: {AlphaConfig.COMPRESSION_LEVEL}")
    print(f"🔒 Защищённых сущностей: {len(AlphaConfig.PROTECTED_ENTITIES)}")
    print(f"🔄 Повторных попыток: {AlphaConfig.OLLAMA_MAX_RETRIES}")
    print("=" * 70)
    
    # Запускаем сервер
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    input("Нажмите Enter для выхода...")