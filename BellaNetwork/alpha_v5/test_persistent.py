from persistent_core import PersistentCore
from pathlib import Path

pc = PersistentCore(Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local"))
print("Состояние:", pc.get_state())

# Добавляем тестовую мысль
pc.add_thought("Тестовая мысль", source="test")

# Проверяем
print("Файл существует?", pc.state_file.exists())