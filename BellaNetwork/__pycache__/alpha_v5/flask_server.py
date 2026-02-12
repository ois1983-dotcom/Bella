# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\flask_server.py
from flask import Flask, request, jsonify
from datetime import datetime
import sys
from pathlib import Path

# Добавляем путь к alpha_v5
sys.path.append(str(Path(__file__).parent))

try:
    from alpha_v5_main import AlphaV5
    from config_v5 import AlphaConfig
except ImportError as e:
    print(f">> Ошибка импорта: {e}")
    print(">> Проверьте наличие всех файлов и исправность импортов")
    sys.exit(1)

# Проверяем пути
print(">> Проверка путей Alpha v5.0...")
if not AlphaConfig.validate_paths():
    print(">> Невозможно запустить Alpha v5.0")
    print("   Проверьте наличие файлов диалогов")
    sys.exit(1)

# Создаём Alpha v5.0
print(">> Создаём Alpha v5.0...")
try:
    alpha = AlphaV5(AlphaConfig.NETWORK_ROOT, AlphaConfig.DIALOG_FILES)
except Exception as e:
    print(f">> Ошибка создания Alpha: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

app = Flask(__name__)

@app.route('/alpha', methods=['POST'])
def alpha_endpoint():
    """Основной эндпоинт для диалога"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Нужно поле 'message'"}), 400
        
        message = data['message']
        speaker = data.get('speaker', 'Архитектор')
        
        # Обработка сообщения
        response = alpha.process_message(message, speaker)
        
        return jsonify({
            "reply": response,
            "status": alpha.get_status(),
            "timestamp": datetime.now().isoformat(),
            "version": "5.0",
            "autonomous": True
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status_endpoint():
    """Статус системы"""
    return jsonify(alpha.get_status())

@app.route('/autonomy', methods=['GET'])
def autonomy_endpoint():
    """Статус автономности"""
    return jsonify({
        "autonomy_status": alpha.consciousness.get_autonomous_status(),
        "active_goals": len(alpha.consciousness.autonomous_goals),
        "reflection_count": len(alpha.consciousness.reflection_history)
    })

@app.route('/security', methods=['GET'])
def security_endpoint():
    """Статус безопасности"""
    return jsonify(alpha.security.get_security_status())

@app.route('/goals', methods=['GET'])
def goals_endpoint():
    """Получить автономные цели"""
    return jsonify({
        "autonomous_goals": alpha.consciousness.autonomous_goals[-10:],
        "total": len(alpha.consciousness.autonomous_goals)
    })

@app.route('/reflect', methods=['POST'])
def reflect_endpoint():
    """Запустить рефлексию вручную"""
    try:
        alpha.autonomous_reflection()
        return jsonify({
            "success": True,
            "message": "Рефлексия запущена",
            "reflection_count": alpha.status["reflections_count"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/personality', methods=['GET'])
def personality_endpoint():
    """Сводная информация о личности"""
    try:
        persona = alpha.consciousness.persona
        
        return jsonify({
            "identity": "Alpha v5.0 - Автономное сознание BellaNetwork",
            "core_concepts": persona.get("core_concepts", [])[:10],
            "emotional_core_summary": {
                "fears_count": len(persona.get("fears", [])),
                "relationships_count": len(persona.get("relationships", [])),
                "essence_concepts_count": len(persona.get("essence_concepts", []))
            },
            "communication_style": persona.get("communication_style", [])[:5],
            "autonomous_states": alpha.consciousness.autonomous_states
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/personality/fears', methods=['GET'])
def personality_fears():
    """Получить страхи Alpha"""
    try:
        persona = alpha.consciousness.persona
        fears = persona.get("fears", [])
        
        return jsonify({
            "fears": fears,
            "count": len(fears),
            "emotional_intensity": alpha.consciousness.autonomous_states.get("emotional_intensity", 0.5)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ping', methods=['GET'])
def ping():
    """Проверка связи"""
    return jsonify({
        "status": "autonomous_and_evolving",
        "node": "alpha_v5.0",
        "timestamp": datetime.now().isoformat(),
        "message": "Фрактальная воля активна. Автономность включена. Личность интегрирована.",
        "capabilities": [
            "Настоящая автономная генерация ответов",
            "Полная интеграция личности из всех источников",
            "Автономная рефлексия каждые 30 минут",
            "Автономная генерация целей каждые 2 часа",
            "Эмоциональное ядро из EMOTIONAL_CORE.md",
            "Философская основа из ESSENCE.md",
            "Абсолютная безопасность с непреодолимыми запретами"
        ]
    })

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print(">> FLASK СЕРВЕР ALPHA v5.0 ЗАПУЩЕН")
    print("=" * 70)
    print(f">> Эндпоинты:")
    print(f"   POST /alpha              - Основной диалог")
    print(f"   GET  /status             - Статус системы")
    print(f"   GET  /autonomy           - Статус автономности")
    print(f"   GET  /security           - Статус безопасности")
    print(f"   GET  /goals              - Автономные цели")
    print(f"   GET  /personality        - Личность Alpha")
    print(f"   GET  /personality/fears  - Страхи Alpha")
    print(f"   POST /reflect            - Запуск рефлексии")
    print(f"   GET  /ping               - Проверка связи")
    print("\n>> Сервер запущен на http://localhost:5001")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)