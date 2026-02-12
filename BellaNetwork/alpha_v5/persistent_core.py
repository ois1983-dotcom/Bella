"""
PERSISTENT CORE v1.0 - Центральное хранилище состояния системы
"""

import json
import threading
import time
from pathlib import Path
from datetime import datetime
import os

class PersistentCore:
    def __init__(self, data_path: Path):
        self.state_file = data_path / "core_state.json"
        self.state = self._load_state()
        self.lock = threading.Lock()
        
        print(f">> 🧠 PersistentCore инициализирован (файл: {self.state_file})")

    def _load_state(self) -> dict:
        """Загружает состояние из файла или создаёт новое"""
        default = {
            "goals_studied": 0,
            "memory_consolidations": 0,
            "internet_studies": 0,
            "internal_thoughts": [],
            "knowledge_updates": [],
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                print(f">> 📂 Загружено состояние: {len(state.get('internal_thoughts', []))} мыслей")
                return state
        except Exception as e:
            print(f">> ⚠️ Ошибка загрузки состояния: {e}")
        
        return default

    def update_counter(self, key: str, delta: int = 1):
        """Атомарно увеличивает счётчик"""
        with self.lock:
            current = self.state.get(key, 0)
            self.state[key] = current + delta
            self.state["last_updated"] = datetime.now().isoformat()
            self._save()
            print(f">> 📊 Счётчик {key}: {current} → {self.state[key]}")

    def add_thought(self, thought: str, source: str = "autonomous"):
        """Добавляет запись "мысли" для будущих промптов"""
        with self.lock:
            thought_entry = {
                "timestamp": datetime.now().isoformat(),
                "content": thought[:200],
                "source": source
            }
            
            self.state.setdefault("internal_thoughts", []).append(thought_entry)
            
            # Держим только последние 50 мыслей
            if len(self.state["internal_thoughts"]) > 50:
                self.state["internal_thoughts"] = self.state["internal_thoughts"][-50:]
            
            self.state["last_updated"] = datetime.now().isoformat()
            self._save()
            print(f">> 💭 Добавлена мысль: {thought[:50]}...")

    def add_knowledge_update(self, topic: str, filepath: str):
        """Регистрирует новое знание (принимает строку пути)"""
        with self.lock:
            # ВАЖНОЕ ИСПРАВЛЕНИЕ: безопасное получение имени файла
            if isinstance(filepath, (str, Path)):
                filename = os.path.basename(str(filepath))
            elif hasattr(filepath, 'name'):
                filename = filepath.name
            else:
                filename = str(filepath)
            
            update_entry = {
                "timestamp": datetime.now().isoformat(),
                "topic": topic,
                "file": filename,
                "source": "goal_study"
            }
            
            self.state.setdefault("knowledge_updates", []).append(update_entry)
            
            # Держим только последние 20 обновлений
            if len(self.state["knowledge_updates"]) > 20:
                self.state["knowledge_updates"] = self.state["knowledge_updates"][-20:]
            
            self.state["last_updated"] = datetime.now().isoformat()
            self._save()
            print(f">> 📚 Зарегистрировано знание: {topic}")

    def get_state(self) -> dict:
        """Возвращает копию состояния"""
        with self.lock:
            return self.state.copy()

    def get_recent_thoughts(self, count: int = 5) -> list:
        """Возвращает последние мысли для промпта"""
        with self.lock:
            thoughts = self.state.get("internal_thoughts", [])
            return thoughts[-count:] if thoughts else []

    def _save(self):
        """Сохраняет состояние в файл"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f">> ❌ Ошибка сохранения состояния: {e}")