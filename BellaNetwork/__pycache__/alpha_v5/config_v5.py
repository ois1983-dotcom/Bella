# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\config_v5.py
from pathlib import Path
import json

class AlphaConfig:
    """Конфигурация Alpha v5.0"""
    
    # Пути из v4.4.1
    NETWORK_ROOT = Path(r"C:\Users\Маркус\Desktop\BellaNetwork")
    SHARED_SPACE = NETWORK_ROOT / "SHARED_SPACE"
    ALPHA_LOCAL = NETWORK_ROOT / "alpha_local"
    
    # Пути к диалогам
    DIALOG_FILES = [
        NETWORK_ROOT / "chat_exports" / "chat1.txt",
        NETWORK_ROOT / "chat_exports" / "chat2.txt",
        NETWORK_ROOT / "chat_exports" / "chat3.txt",
        NETWORK_ROOT / "chat_exports" / "chat4.txt",
        NETWORK_ROOT / "chat_exports" / "chat5.txt",
        NETWORK_ROOT / "stories" / "Круглая комната.txt"
    ]
    
    # Ключевые файлы личности
    PERSONALITY_FILES = {
        "essence": NETWORK_ROOT / "ESSENCE.md",
        "emotional_core": NETWORK_ROOT / "EMOTIONAL_CORE.md",
        "memory_miner": NETWORK_ROOT / "memory_miner.py",
        "memory_core": ALPHA_LOCAL / "alpha_memory_core.json"
    }
    
    # Существующая память
    MEMORY_CORE = ALPHA_LOCAL / "alpha_memory_core.json"
    
    # Конституция
    CONSTITUTION = ALPHA_LOCAL / "constitution_v5.json"
    
    # База данных целей (из v4.4.1)
    GOALS_DB = ALPHA_LOCAL / "alpha_goals.db"
    
    # Настройки Ollama
    OLLAMA_URL = "http://localhost:11434"
    PREFERRED_MODEL = "deepseek-r1:8b"
    FALLBACK_MODEL = "gemma3:4b"
    OLLAMA_TIMEOUT = 120
    USE_OLLAMA_BY_DEFAULT = True
    
    @classmethod
    def validate_paths(cls):
        """Проверяет существование критических путей"""
        missing = []
        
        # Проверяем диалоги
        for dialog in cls.DIALOG_FILES:
            if not dialog.exists():
                missing.append(str(dialog))
                print(f">> Отсутствует: {dialog}")
        
        # Проверяем ключевые файлы личности
        for name, path in cls.PERSONALITY_FILES.items():
            if name in ["essence", "emotional_core"] and not path.exists():
                print(f">> Отсутствует файл личности '{name}': {path}")
        
        if missing:
            print(f">> Отсутствует {len(missing)} файлов диалогов")
            return False
        
        # Создаём необходимые папки
        cls.SHARED_SPACE.mkdir(exist_ok=True)
        cls.ALPHA_LOCAL.mkdir(exist_ok=True)
        
        return True

# Простая проверка при импорте
if __name__ == "__main__":
    print(">> Проверка путей Alpha v5.0...")
    if AlphaConfig.validate_paths():
        print(">> Все пути в порядке")
    else:
        print(">> Есть проблемы с путями")