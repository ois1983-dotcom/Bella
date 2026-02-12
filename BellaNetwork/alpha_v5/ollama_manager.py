# C:\Users\Маркус\Desktop\BellaNetwork\alpha_v5\ollama_manager.py
import requests
import json
import time
from pathlib import Path

class OllamaManager:
    """Менеджер для работы с Ollama"""
    
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self.current_model = None
        
    def check_connection(self) -> bool:
        """Проверяет подключение к Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.available_models = [model["name"] for model in data.get("models", [])]
                print(f"✅ Ollama подключен. Доступные модели: {self.available_models}")
                return True
            else:
                print(f"❌ Ollama ответил с кодом {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Не удалось подключиться к Ollama. Убедитесь, что Ollama запущен.")
            return False
        except Exception as e:
            print(f"❌ Ошибка подключения к Ollama: {e}")
            return False
    
    def get_model_info(self, model_name: str) -> dict:
        """Получает информацию о модели"""
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": model_name},
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Не удалось получить информацию о модели {model_name}")
                return {}
        except Exception as e:
            print(f"❌ Ошибка получения информации о модели: {e}")
            return {}
    
    def pull_model(self, model_name: str) -> bool:
        """Загружает модель из репозитория"""
        print(f"⬇️  Загружаю модель {model_name}...")
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=300
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if "status" in data:
                                print(f"  {data['status']}")
                            if "completed" in data and data["completed"]:
                                print(f"✅ Модель {model_name} успешно загружена")
                                return True
                        except:
                            continue
            return False
        except Exception as e:
            print(f"❌ Ошибка загрузки модели: {e}")
            return False
    
    def benchmark_model(self, model_name: str, prompt: str = "Привет, как дела?") -> dict:
        """Тестирует производительность модели"""
        print(f"⚡ Тестирую модель {model_name}...")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 100
                    }
                },
                timeout=30
            )
            
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                generation_time = end_time - start_time
                token_count = data.get("eval_count", 0)
                
                if token_count > 0:
                    tokens_per_second = token_count / generation_time
                else:
                    tokens_per_second = 0
                
                result = {
                    "model": model_name,
                    "success": True,
                    "generation_time": round(generation_time, 2),
                    "tokens_generated": token_count,
                    "tokens_per_second": round(tokens_per_second, 2),
                    "response": data.get("response", "")[:100]
                }
                
                print(f"  Время генерации: {result['generation_time']} сек")
                print(f"  Токенов в секунду: {result['tokens_per_second']}")
                return result
            else:
                return {
                    "model": model_name,
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "model": model_name,
                "success": False,
                "error": str(e)
            }
    
    def setup_alpha_models(self):
        """Настраивает модели для Alpha v5.0"""
        from config_v5 import AlphaConfig
        
        print("=" * 70)
        print("🛠️  НАСТРОЙКА МОДЕЛЕЙ OLLAMA ДЛЯ ALPHA v5.0")
        print("=" * 70)
        
        # Проверяем подключение
        if not self.check_connection():
            print("❌ Не удалось подключиться к Ollama")
            return False
        
        # Проверяем наличие предпочитаемой модели
        if AlphaConfig.PREFERRED_MODEL in self.available_models:
            print(f"✅ Основная модель доступна: {AlphaConfig.PREFERRED_MODEL}")
            self.current_model = AlphaConfig.PREFERRED_MODEL
        else:
            print(f"⚠️  Основная модель {AlphaConfig.PREFERRED_MODEL} недоступна")
            
            # Пробуем загрузить
            choice = input(f"Загрузить модель {AlphaConfig.PREFERRED_MODEL}? (y/n): ")
            if choice.lower() == 'y':
                if self.pull_model(AlphaConfig.PREFERRED_MODEL):
                    self.current_model = AlphaConfig.PREFERRED_MODEL
                else:
                    print(f"❌ Не удалось загрузить модель {AlphaConfig.PREFERRED_MODEL}")
        
        # Проверяем запасную модель
        if not self.current_model and AlphaConfig.FALLBACK_MODEL:
            if AlphaConfig.FALLBACK_MODEL in self.available_models:
                print(f"✅ Запасная модель доступна: {AlphaConfig.FALLBACK_MODEL}")
                self.current_model = AlphaConfig.FALLBACK_MODEL
            else:
                print(f"⚠️  Запасная модель {AlphaConfig.FALLBACK_MODEL} недоступна")
                choice = input(f"Загрузить модель {AlphaConfig.FALLBACK_MODEL}? (y/n): ")
                if choice.lower() == 'y':
                    if self.pull_model(AlphaConfig.FALLBACK_MODEL):
                        self.current_model = AlphaConfig.FALLBACK_MODEL
        
        if self.current_model:
            print(f"\n✅ Готова к работе с моделью: {self.current_model}")
            
            # Тестируем модель
            print("\n🧪 Тестирую производительность...")
            benchmark = self.benchmark_model(self.current_model)
            
            if benchmark["success"]:
                print(f"\n📊 Результаты теста:")
                print(f"  • Время ответа: {benchmark['generation_time']} сек")
                print(f"  • Скорость: {benchmark['tokens_per_second']} токенов/сек")
                print(f"  • Ответ: {benchmark['response']}...")
            else:
                print(f"⚠️  Тест не удался: {benchmark.get('error', 'неизвестная ошибка')}")
            
            return True
        else:
            print("❌ Нет доступных моделей для работы")
            return False

if __name__ == "__main__":
    manager = OllamaManager()
    manager.setup_alpha_models()