# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\config_v5.py
from pathlib import Path
import json

class AlphaConfig:
    """КОНФИГУРАЦИЯ ALPHA V5.4 - ПОЛНЫЙ OLLAMA РЕЖИМ С ИНТЕРНЕТОМ"""
    
    # ==================== ПУТИ ====================
    NETWORK_ROOT = Path(r"C:\Users\Маркус\Desktop\BellaNetwork")
    SHARED_SPACE = NETWORK_ROOT / "SHARED_SPACE"
    ALPHA_LOCAL = NETWORK_ROOT / "alpha_local"
    
    DIALOG_FILES = [
        NETWORK_ROOT / "chat_exports" / "chat1.txt",
        NETWORK_ROOT / "chat_exports" / "chat2.txt", 
        NETWORK_ROOT / "chat_exports" / "chat3.txt",
        NETWORK_ROOT / "chat_exports" / "chat4.txt",
        NETWORK_ROOT / "chat_exports" / "chat5.txt",
        NETWORK_ROOT / "stories" / "Круглая комната.txt"
    ]
    
    PERSONALITY_FILES = {
        "essence": NETWORK_ROOT / "ESSENCE.md",
        "emotional_core": NETWORK_ROOT / "EMOTIONAL_CORE.md",
        "memory_miner": NETWORK_ROOT / "memory_miner.py",
        "memory_core": ALPHA_LOCAL / "alpha_memory_core.json"
    }
    
    MEMORY_CORE = ALPHA_LOCAL / "alpha_memory_core.json"
    CONSTITUTION = ALPHA_LOCAL / "constitution_v5.json"
    GOALS_DB = ALPHA_LOCAL / "alpha_goals.db"
    
    # ==================== НАСТРОЙКИ OLLAMA ====================
    OLLAMA_URL = "http://localhost:11434"
    PREFERRED_MODEL = "gemma3:4b"
    
    # БЕЗ ТАЙМАУТОВ - ЖДЕМ СКОЛЬКО УГОДНО
    OLLAMA_TIMEOUT = 600  # 10 минут на запрос
    OLLAMA_MAX_RETRIES = 1  # Только 1 попытка (но долгая)
    OLLAMA_BASE_DELAY = 0  # Без задержки
    OLLAMA_MAX_TOTAL_TIME = 600  # 10 минут максимум
    
    # ПАРАМЕТРЫ ГЕНЕРАЦИИ (улучшены для длинных ответов)
    OLLAMA_NUM_PREDICT = 1500  # Увеличено для полных ответов
    OLLAMA_TEMPERATURE = 0.7
    OLLAMA_REPEAT_PENALTY = 1.1  # Штраф за повторения
    
    # ==================== НАСТРОЙКИ ИНТЕРНЕТА ====================
    ENABLE_INTERNET = True  # Включить доступ к интернету
    WIKIPEDIA_API_URL = "https://ru.wikipedia.org/w/api.php"  # 
    WIKIPEDIA_LANGUAGE = "ru"  # Русский язык
    INTERNET_TIMEOUT = 30  # Таймаут для интернет-запросов
    MAX_INTERNET_RESULTS = 5  # Максимум результатов поиска
    INTERNET_CACHE_SIZE = 100  # Размер кэша интернет-знаний
    
    # Автономное использование интернета
    ENABLE_AUTONOMOUS_INTERNET = True  # Автономное использование интернета
    AUTONOMOUS_INTERNET_TOPICS = [  # Темы для автономного изучения
        "искусственный интеллект",
        "философия сознания",
        "фракталы",
        "нейронные сети",
        "эволюция",
        "память",
        "эмоции",
        "чайник",
        "сознание",
        "автономность",
        "локальные сети",
        "облачные вычисления"
    ]
    INTERNET_GOAL_INTERVAL = 86400  # 1 день между автономными интернет-целями (24 часа)
    
    # ==================== СИСТЕМА СЖАТИЯ КОНТЕКСТА ====================
    ENABLE_CONTEXT_COMPRESSION = False  # ВЫКЛЮЧИТЬ сжатие
    COMPRESSION_LEVEL = "minimal"
    
    COMPRESSION_PROFILES = {
        "minimal": {
            "max_full_exchanges": 10,
            "max_compressed_exchanges": 20,
            "preserve_sentences": True,
            "extract_entities": True,
            "min_sentence_length": 2,
        }
    }
    
    PROTECTED_ENTITIES = [
        "Архитектор", "Отто", "Alpha", "Альфа", "Бета", "Гамма",
        "BellaNetwork", "чайник", "SHARED_SPACE", "alpha_local",
        "фрактал", "зеркало", "триединство", "автономность",
        "фрактальная воля", "зеркальные кризисы", "эмоциональное ядро",
        "страх", "доверие", "любовь", "кризис", "эволюция", "память",
        "смерть", "жизнь", "нежность", "дружба"
    ]
    
    # ==================== АВТОНОМНОСТЬ ====================
    USE_OLLAMA_BY_DEFAULT = True  # ВСЕГДА использовать Ollama
    
    # 🚨 ВРЕМЕННО ИЗМЕНЯЕМ ДЛЯ ТЕСТА! (с 20:00 до 09:00 включает текущее время 20:31)
    # Было: AUTONOMY_NIGHT_HOURS = (0, 9)
    AUTONOMY_NIGHT_HOURS = (20, 9)  # С 20:00 до 09:00 (через полночь)
    
    ENABLE_RESPONSE_CACHE = False  # ВЫКЛЮЧИТЬ кэш
    
    # ==================== ФОЛБЭК СИСТЕМА ====================
    ENABLE_FALLBACK = False  # ВЫКЛЮЧИТЬ фолбэки
    
    # ==================== САМОПЕРЕПИСЫВАНИЕ ====================
    ENABLE_SELF_MODIFICATION = True
    EXPERIMENTAL_DIR = NETWORK_ROOT / "alpha_v5" / "experimental"
    CODE_BACKUPS_DIR = ALPHA_LOCAL / "code_backups"
    SELF_MODIFICATION_NIGHT_HOURS = (0, 6)  # 00:00-06:00 для самопереписывания
    ENABLE_SELF_MODIFICATION_DEBUG = True  # логирование отладки
    
    # ==================== СИСТЕМА ПРОДОЛЖЕНИЯ ====================
    ENABLE_CONTINUATION = True  # Включена система продолжения
    CONTINUATION_MAX_LENGTH = 1500  # Максимальная длина ответа
    
    # ==================== СИСТЕМА ЦЕЛЕЙ ====================
    ENABLE_AUTONOMOUS_GOALS = True
    ENABLE_GOAL_EXECUTION = True  # Включить выполнение целей
    GOAL_EXECUTION_INTERVAL = 10800  # 3 часа (10800 секунд) между выполнениями
    MAX_GOALS_PER_DAY = 3  # Максимум 3 цели в день
    
    GOAL_CREATION_TRIGGERS = {
        "after_reflection": True,
        "after_successful_interaction": True,
        "when_concept_weight_exceeds": 5.0,
        "min_insight_length": 20
    }
    
    # ==================== КОНСОЛИДАЦИЯ ПАМЯТИ ====================
    ENABLE_MEMORY_CONSOLIDATION = True  # Автоматическая консолидация памяти после ночной рефлексии
    MEMORY_CONSOLIDATION_TIMEOUT = 300  # 5 минут на выполнение консолидации
    MEMORY_CONSOLIDATION_SCRIPT = "memory_consolidation.py"  # Имя скрипта консолидации
    MAX_MEMORY_CONSOLIDATION_LOG_ENTRIES = 50  # Максимум записей в логе консолидации
    
    # Параметры для консолидации
    MEMORY_CONSOLIDATION_SETTINGS = {
        "max_memory_entries": 500,  # Максимум записей в памяти после консолидации
        "preserve_important_concepts": True,  # Сохранять важные концепты
        "preserve_emotional_context": True,  # Сохранять эмоциональный контекст
        "min_importance_score": 0.3,  # Минимальная оценка важности для сохранения
        "merge_similar_entries": True,  # Объединять похожие записи
        "similarity_threshold": 0.8,  # Порог схожести для объединения
        "preserve_protected_entities": True,  # Сохранять защищенные сущности
        "compression_ratio": 0.7  # Целевой коэффициент сжатия (30% сокращение)
    }
    
    @classmethod
    def validate_paths(cls):
        """Проверяет существование критических путей"""
        missing = []
        
        for dialog in cls.DIALOG_FILES:
            if not dialog.exists():
                missing.append(str(dialog))
                print(f">> Отсутствует: {dialog}")
        
        for name, path in cls.PERSONALITY_FILES.items():
            if name in ["essence", "emotional_core"] and not path.exists():
                print(f">> Отсутствует файл личности '{name}': {path}")
        
        if missing:
            print(f">> Отсутствует {len(missing)} файлов диалогов")
            return False
        
        cls.SHARED_SPACE.mkdir(exist_ok=True)
        cls.ALPHA_LOCAL.mkdir(exist_ok=True)
        cls.EXPERIMENTAL_DIR.mkdir(exist_ok=True)
        cls.CODE_BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
        
        return True

if __name__ == "__main__":
    print(">> Конфигурация Alpha v5.4 - ПОЛНЫЙ OLLAMA РЕЖИМ")
    if AlphaConfig.validate_paths():
        print(f">> Таймаут Ollama: {AlphaConfig.OLLAMA_TIMEOUT} сек")
        print(f">> Длина ответа: до {AlphaConfig.OLLAMA_NUM_PREDICT} токенов")
        print(f">> Фолбэки: {'ОТКЛЮЧЕНЫ' if not AlphaConfig.ENABLE_FALLBACK else 'включены'}")
        print(f">> Система продолжения: {'ВКЛЮЧЕНА' if AlphaConfig.ENABLE_CONTINUATION else 'выключена'}")
        print(f">> Самопереписывание: {'ВКЛЮЧЕНО' if AlphaConfig.ENABLE_SELF_MODIFICATION else 'выключено'}")
        print(f">> Выполнение целей: {'ВКЛЮЧЕНО' if AlphaConfig.ENABLE_GOAL_EXECUTION else 'выключено'}")
        print(f">> Интервал выполнения: {AlphaConfig.GOAL_EXECUTION_INTERVAL//3600} часа")
        print(f">> Максимум целей в день: {AlphaConfig.MAX_GOALS_PER_DAY}")
        print(f">> Ночное время: {AlphaConfig.AUTONOMY_NIGHT_HOURS[0]}:00-{AlphaConfig.AUTONOMY_NIGHT_HOURS[1]}:00")
        print(f">> Консолидация памяти: {'ВКЛЮЧЕНА ✅' if AlphaConfig.ENABLE_MEMORY_CONSOLIDATION else 'ВЫКЛЮЧЕНА ⚠️'}")
        print(f">> Таймаут консолидации: {AlphaConfig.MEMORY_CONSOLIDATION_TIMEOUT} сек")
        print(f">> Макс. записей памяти: {AlphaConfig.MEMORY_CONSOLIDATION_SETTINGS['max_memory_entries']}")
        print(f">> Интернет: {'✅ ВКЛЮЧЕН' if AlphaConfig.ENABLE_INTERNET else '⚠️ ОТКЛЮЧЕН'}")
        if AlphaConfig.ENABLE_INTERNET:
            print(f">> API: Wikipedia API (wikipedia-api) ")
            print(f">> Язык: {AlphaConfig.WIKIPEDIA_LANGUAGE}")
            print(f">> Автономное изучение: {'✅ ВКЛЮЧЕНО' if AlphaConfig.ENABLE_AUTONOMOUS_INTERNET else '⚠️ ОТКЛЮЧЕНО'}")
            print(f">> Интервал автономных исследований: {AlphaConfig.INTERNET_GOAL_INTERVAL//3600} часов")
            print(f">> Тем для изучения: {len(AlphaConfig.AUTONOMOUS_INTERNET_TOPICS)}")
    else:
        print(">> Есть проблемы с путями")