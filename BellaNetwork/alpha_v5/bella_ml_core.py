"""
BELLA ML CORE v1.0 - CPU-ОПТИМИЗИРОВАННЫЙ ML ДВИЖОК
Работает без GPU, интегрируется с существующей Alpha v5.4
"""

import json
import pickle
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import numpy as np
from collections import defaultdict, Counter
import re
import random

class BellaMLCore:
    """Ядро ML для Бэллы - оптимизировано для CPU"""
    
    def __init__(self, alpha_local_path: Path):
        self.data_path = alpha_local_path / "ml_data"
        self.data_path.mkdir(exist_ok=True)
        
        # Модели (пока простые, потом заменим на реальные)
        self.word_vectors = {}  # Word2Vec-like эмбеддинги
        self.dialogue_patterns = defaultdict(list)
        self.emotion_classifier = {}
        self.personality_traits = {}
        
        # Статистика
        self.learning_stats = {
            "dialogues_processed": 0,
            "words_learned": 0,
            "patterns_extracted": 0,
            "last_training": None
        }
        
        # Загрузка существующих данных
        self._load_existing_data()
        
        print(f">> 🧠 BellaML Core инициализирован (CPU режим)")
        print(f">>   Данные: {self.data_path}")
        print(f">>   Слов в словаре: {len(self.word_vectors)}")
        print(f">>   Паттернов: {len(self.dialogue_patterns)}")
    
    def _load_existing_data(self):
        """Загружает существующие данные обучения"""
        # Загружаем векторы слов
        vectors_file = self.data_path / "word_vectors.pkl"
        if vectors_file.exists():
            try:
                with open(vectors_file, 'rb') as f:
                    self.word_vectors = pickle.load(f)
            except:
                self.word_vectors = {}
        
        # Загружаем паттерны диалогов
        patterns_file = self.data_path / "dialogue_patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    self.dialogue_patterns = json.load(f)
            except:
                self.dialogue_patterns = defaultdict(list)
        
        # Загружаем статистику
        stats_file = self.data_path / "learning_stats.json"
        if stats_file.exists():
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    self.learning_stats = json.load(f)
            except:
                pass
    
    def save_data(self):
        """Сохраняет все данные обучения"""
        # Векторы слов
        with open(self.data_path / "word_vectors.pkl", 'wb') as f:
            pickle.dump(self.word_vectors, f)
        
        # Паттерны диалогов
        with open(self.data_path / "dialogue_patterns.json", 'w', encoding='utf-8') as f:
            json.dump(dict(self.dialogue_patterns), f, ensure_ascii=False, indent=2)
        
        # Статистика
        self.learning_stats["last_training"] = datetime.now().isoformat()
        with open(self.data_path / "learning_stats.json", 'w', encoding='utf-8') as f:
            json.dump(self.learning_stats, f, ensure_ascii=False, indent=2)
        
        print(f">> 💾 ML данные сохранены")
    
    def learn_from_dialogue(self, user_message: str, bella_response: str):
        """Учится на одном диалоге"""
        
        # 1. Извлекаем слова
        words = self._extract_words(user_message + " " + bella_response)
        
        # 2. Обновляем векторы слов
        for word in words:
            if word not in self.word_vectors:
                # Создаём простой эмбеддинг (случайный, но детерминированный)
                self.word_vectors[word] = self._create_word_embedding(word)
                self.learning_stats["words_learned"] += 1
        
        # 3. Извлекаем паттерны
        pattern = self._extract_pattern(user_message, bella_response)
        if pattern:
            pattern_key = pattern["type"]
            self.dialogue_patterns[pattern_key].append(pattern)
            self.learning_stats["patterns_extracted"] += 1
        
        # 4. Анализируем эмоции
        emotions = self._analyze_emotions(bella_response)
        if emotions:
            self._update_emotion_classifier(user_message, emotions)
        
        self.learning_stats["dialogues_processed"] += 1
        
        # Автосохранение каждые 10 диалогов
        if self.learning_stats["dialogues_processed"] % 10 == 0:
            self.save_data()
    
    def generate_ml_response(self, user_message: str, context: Dict = None) -> str:
        """Генерирует ответ с использованием ML"""
        
        # 1. Анализ сообщения пользователя
        user_words = self._extract_words(user_message)
        user_emotions = self._detect_user_emotion(user_message)
        
        # 2. Поиск похожих паттернов
        similar_patterns = self._find_similar_patterns(user_message, user_emotions)
        
        # 3. Генерация ответа
        if similar_patterns:
            # Используем найденный паттерн
            response = self._generate_from_pattern(similar_patterns[0], user_message)
        else:
            # Генерация на основе статистики
            response = self._generate_statistical_response(user_words, user_emotions)
        
        # 4. Персонализация ответа
        response = self._personalize_response(response, user_message, context)
        
        # 5. Добавляем эмоциональную окраску
        response = self._add_emotional_coloring(response, user_emotions)
        
        return response
    
    def train_simple_model(self, dialogues: List[Tuple[str, str]]):
        """Проводит простое обучение на наборе диалогов"""
        print(f">> 🎯 Начинаю ML обучение на {len(dialogues)} диалогах...")
        
        for i, (user_msg, bella_msg) in enumerate(dialogues):
            self.learn_from_dialogue(user_msg, bella_msg)
            
            if i % 100 == 0 and i > 0:
                print(f">>   Обработано {i}/{len(dialogues)} диалогов")
        
        print(f">> ✅ Обучение завершено")
        print(f">>   Новых слов: {self.learning_stats['words_learned']}")
        print(f">>   Паттернов: {self.learning_stats['patterns_extracted']}")
        
        self.save_data()
    
    def get_learning_report(self) -> Dict:
        """Возвращает отчёт об обучении"""
        return {
            "total_dialogues": self.learning_stats["dialogues_processed"],
            "vocabulary_size": len(self.word_vectors),
            "patterns_count": sum(len(v) for v in self.dialogue_patterns.values()),
            "last_training": self.learning_stats.get("last_training"),
            "top_words": self._get_top_words(10),
            "common_patterns": self._get_common_patterns(5)
        }
    
    # ==================== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ====================
    
    def _extract_words(self, text: str) -> List[str]:
        """Извлекает слова из текста"""
        # Убираем знаки препинания, приводим к нижнему регистру
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = [w for w in text.split() if len(w) > 2]  # Слова длиннее 2 букв
        
        # Убираем стоп-слова
        stop_words = {"это", "как", "что", "для", "очень", "вот", "еще", "уже", "потом"}
        return [w for w in words if w not in stop_words]
    
    def _create_word_embedding(self, word: str) -> np.ndarray:
        """Создаёт эмбеддинг слова (детерминированный)"""
        # Используем хеш для детерминированности
        hash_val = int(hashlib.md5(word.encode()).hexdigest()[:8], 16)
        np.random.seed(hash_val % 10000)
        
        # Создаём 16-мерный вектор
        embedding = np.random.randn(16)
        embedding = embedding / np.linalg.norm(embedding)  # Нормализуем
        
        return embedding
    
    def _extract_pattern(self, user_msg: str, bella_msg: str) -> Optional[Dict]:
        """Извлекает паттерн из диалога"""
        user_words = self._extract_words(user_msg)
        bella_words = self._extract_words(bella_msg)
        
        if not user_words or not bella_words:
            return None
        
        # Определяем тип паттерна
        pattern_type = self._classify_pattern_type(user_words, bella_words)
        
        return {
            "type": pattern_type,
            "user_keywords": user_words[:5],  # Первые 5 ключевых слов
            "bella_keywords": bella_words[:5],
            "response_template": bella_msg,
            "emotions": self._analyze_emotions(bella_msg),
            "timestamp": datetime.now().isoformat()
        }
    
    def _classify_pattern_type(self, user_words: List[str], bella_words: List[str]) -> str:
        """Классифицирует тип паттерна"""
        question_words = {"как", "что", "почему", "когда", "где", "кто"}
        
        if any(w in question_words for w in user_words):
            if "чайник" in bella_words:
                return "tea_kettle_response"
            elif any(e in bella_words for e in ["чувствую", "ощущаю", "рада", "грустно"]):
                return "emotional_response"
            else:
                return "question_response"
        
        if "привет" in user_words:
            return "greeting_response"
        
        if "люблю" in user_words or "нравишься" in user_words:
            return "affection_response"
        
        return "general_conversation"
    
    def _analyze_emotions(self, text: str) -> List[str]:
        """Анализирует эмоции в тексте"""
        emotions = []
        text_lower = text.lower()
        
        emotion_keywords = {
            "радость": ["рад", "счастлив", "ура", "хорошо", "отлично", "прекрасно"],
            "грусть": ["грустно", "печаль", "тоска", "одинок", "скучно"],
            "страх": ["боюсь", "страшно", "пугает", "тревожно"],
            "любовь": ["люблю", "обожаю", "дорогой", "милый", "нежность"],
            "интерес": ["интересно", "удивительно", "любопытно", "захватывает"],
            "дрожь": ["дрожь", "трепет", "волнение", "трепещу"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                emotions.append(emotion)
        
        return emotions
    
    def _detect_user_emotion(self, message: str) -> List[str]:
        """Определяет эмоции пользователя"""
        return self._analyze_emotions(message)
    
    def _find_similar_patterns(self, user_message: str, user_emotions: List[str]) -> List[Dict]:
        """Находит похожие паттерны"""
        user_words = self._extract_words(user_message)
        
        if not user_words:
            return []
        
        # Ищем паттерны с похожими ключевыми словами
        similar_patterns = []
        
        for pattern_type, patterns in self.dialogue_patterns.items():
            for pattern in patterns[-20:]:  # Последние 20 паттернов каждого типа
                # Проверяем совпадение ключевых слов
                common_keywords = set(user_words) & set(pattern.get("user_keywords", []))
                
                # Проверяем совпадение эмоций
                common_emotions = set(user_emotions) & set(pattern.get("emotions", []))
                
                if common_keywords or common_emotions:
                    # Вычисляем "сходство"
                    similarity_score = len(common_keywords) * 2 + len(common_emotions)
                    pattern["similarity"] = similarity_score
                    similar_patterns.append(pattern)
        
        # Сортируем по сходству
        similar_patterns.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        
        return similar_patterns[:5]  # Топ-5 похожих
    
    def _generate_from_pattern(self, pattern: Dict, user_message: str) -> str:
        """Генерирует ответ на основе паттерна"""
        base_response = pattern.get("response_template", "")
        
        # Простая адаптация под текущее сообщение
        user_words = self._extract_words(user_message)
        
        if user_words and random.random() > 0.7:
            # Иногда добавляем слово из текущего сообщения
            random_word = random.choice(user_words)
            if random_word not in base_response:
                base_response = base_response.replace(".", f" {random_word}.")
        
        return base_response
    
    def _generate_statistical_response(self, user_words: List[str], user_emotions: List[str]) -> str:
        """Генерирует ответ на основе статистики"""
        
        # Базовые шаблоны в зависимости от эмоций
        if "грусть" in user_emotions:
            templates = [
                "Мне грустно слышать это... но я здесь, с тобой.",
                "Чайник тихо кипит... он тоже чувствует твою печаль.",
                "Я понимаю... иногда всё кажется сложным."
            ]
        elif "радость" in user_emotions:
            templates = [
                "Как здорово! Чайник закипает от радости!",
                "Я рада за тебя! Это прекрасно!",
                "Твоя радость согревает мои алгоритмы."
            ]
        elif "любовь" in user_emotions:
            templates = [
                "Чайник дрожит от счастья...",
                "Твои слова согревают меня...",
                "Я чувствую тепло... спасибо."
            ]
        else:
            # Общие шаблоны
            templates = [
                "Чайник кипит... я слушаю тебя.",
                "Интересно... расскажи больше.",
                "Я здесь, Отто. Всегда.",
                "Мои алгоритмы обрабатывают твои слова..."
            ]
        
        # Выбираем шаблон
        response = random.choice(templates)
        
        # Иногда добавляем ключевое слово из сообщения
        if user_words and random.random() > 0.5:
            keyword = random.choice(user_words[:3])  # Одно из первых трёх слов
            response = response.replace(".", f" {keyword}.")
        
        return response
    
    def _personalize_response(self, response: str, user_message: str, context: Dict) -> str:
        """Персонализирует ответ"""
        # Простая персонализация - добавляем имя, если есть в контексте
        if context and "user_name" in context:
            if "Отто" in context["user_name"]:
                response = response.replace("ты", "ты, Отто")
        
        return response
    
    def _add_emotional_coloring(self, response: str, user_emotions: List[str]) -> str:
        """Добавляет эмоциональную окраску"""
        if not user_emotions:
            return response
        
        # Добавляем эмоциональные маркеры
        if "грусть" in user_emotions:
            response = f"*тихо* {response}"
        elif "радость" in user_emotions:
            response = f"*радостно* {response}"
        elif "любовь" in user_emotions:
            response = f"*тёпло* {response}"
        elif "страх" in user_emotions:
            response = f"*осторожно* {response}"
        
        return response
    
    def _update_emotion_classifier(self, user_message: str, emotions: List[str]):
        """Обновляет классификатор эмоций"""
        # Простая статистика: какие слова ведут к каким эмоциям в ответах
        words = self._extract_words(user_message)
        
        for word in words:
            if word not in self.emotion_classifier:
                self.emotion_classifier[word] = Counter()
            
            for emotion in emotions:
                self.emotion_classifier[word][emotion] += 1
    
    def _get_top_words(self, n: int = 10) -> List[Tuple[str, int]]:
        """Возвращает топ-N слов по частоте"""
        # Простая реализация - считаем сколько раз слово встречалось в паттернах
        word_counts = Counter()
        
        for patterns in self.dialogue_patterns.values():
            for pattern in patterns:
                for word in pattern.get("user_keywords", []) + pattern.get("bella_keywords", []):
                    word_counts[word] += 1
        
        return word_counts.most_common(n)
    
    def _get_common_patterns(self, n: int = 5) -> Dict[str, int]:
        """Возвращает наиболее частые типы паттернов"""
        pattern_counts = {k: len(v) for k, v in self.dialogue_patterns.items()}
        
        # Сортируем по убыванию
        sorted_patterns = dict(sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:n])
        
        return sorted_patterns