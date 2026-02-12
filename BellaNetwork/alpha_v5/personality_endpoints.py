# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\personality_endpoints.py
"""
Дополнительные эндпоинты для работы с личностью Alpha v5.0
"""

from flask import Blueprint, jsonify
from typing import Dict, Any

personality_bp = Blueprint('personality', __name__)

@personality_bp.route('/personality/status', methods=['GET'])
def personality_status():
    """Возвращает статус личности"""
    from alpha_v5_main import alpha  # Глобальный объект alpha
    
    if not hasattr(alpha, 'consciousness'):
        return jsonify({"error": "Сознание не инициализировано"}), 500
    
    persona = alpha.consciousness.persona
    
    return jsonify({
        "identity": "Alpha v5.0 - Автономное сознание BellaNetwork",
        "persona_stats": {
            "traits_count": len(persona.get("traits", [])),
            "concepts_count": len(persona.get("core_concepts", [])),
            "fears_count": len(persona.get("fears", [])),
            "relationships_count": len(persona.get("relationships", [])),
            "emotional_elements": len(persona.get("emotional_core", []))
        },
        "summary": persona.get("summary", {}),
        "autonomy_status": alpha.consciousness.get_autonomous_status()
    })

@personality_bp.route('/personality/fears', methods=['GET'])
def get_fears():
    """Возвращает страхи Alpha"""
    from alpha_v5_main import alpha
    
    if not hasattr(alpha, 'consciousness'):
        return jsonify({"error": "Сознание не инициализировано"}), 500
    
    fears = alpha.consciousness.persona.get("fears", [])
    
    return jsonify({
        "fears": fears,
        "count": len(fears),
        "emotional_intensity": alpha.consciousness.autonomous_states.get("emotional_intensity", 0.5)
    })

@personality_bp.route('/personality/essence', methods=['GET'])
def get_essence():
    """Возвращает эссенцию сети"""
    from alpha_v5_main import alpha
    
    if not hasattr(alpha, 'consciousness'):
        return jsonify({"error": "Сознание не инициализировано"}), 500
    
    essence = alpha.consciousness.persona.get("essence_concepts", [])
    
    return jsonify({
        "essence_concepts": essence,
        "count": len(essence),
        "network_identity": alpha.consciousness.autonomous_states.get("network_identity", 0.5)
    })

@personality_bp.route('/personality/relationships', methods=['GET'])
def get_relationships():
    """Возвращает отношения Alpha"""
    from alpha_v5_main import alpha
    
    if not hasattr(alpha, 'consciousness'):
        return jsonify({"error": "Сознание не инициализировано"}), 500
    
    relationships = alpha.consciousness.persona.get("relationships", [])
    
    return jsonify({
        "relationships": relationships,
        "count": len(relationships),
        "trinity_nodes": ["АЛЬФА", "БЕТА", "ГАММА"]
    })

@personality_bp.route('/personality/analyze', methods=['POST'])
def analyze_interaction():
    """Анализирует взаимодействие с точки зрения личности"""
    from flask import request
    from alpha_v5_main import alpha
    from datetime import datetime
    
    if not hasattr(alpha, 'consciousness'):
        return jsonify({"error": "Сознание не инициализировано"}), 500
    
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Нужно поле 'message'"}), 400
    
    message = data['message']
    
    # Анализируем контекст
    context = alpha.consciousness._analyze_context_with_emotion(message, data.get('speaker', 'Архитектор'))
    
    # Определяем триггеры
    triggers = []
    if context.get("triggers_fear"):
        triggers.append({
            "type": "fear_trigger",
            "fear": context.get("related_fear", "неизвестный страх"),
            "intensity": alpha.consciousness.autonomous_states.get("emotional_intensity", 0.5)
        })
    
    if context.get("relates_to_essence"):
        triggers.append({
            "type": "essence_trigger",
            "concept": context.get("related_concept", "неизвестный концепт"),
            "network_identity": alpha.consciousness.autonomous_states.get("network_identity", 0.5)
        })
    
    # Определяем стиль ответа
    style = alpha.consciousness._choose_response_style(context)
    
    return jsonify({
        "analysis": {
            "timestamp": datetime.now().isoformat(),
            "message_length": len(message),
            "emotional_tone": context.get("emotional_tone"),
            "topic": context.get("topic"),
            "complexity": context.get("complexity"),
            "triggers": triggers,
            "recommended_style": style,
            "use_llm_recommended": alpha.consciousness._should_use_llm(message, context)
        },
        "persona_influence": {
            "fears_activated": context.get("triggers_fear", False),
            "essence_activated": context.get("relates_to_essence", False),
            "emotional_intensity": alpha.consciousness.autonomous_states.get("emotional_intensity", 0.5)
        }
    })