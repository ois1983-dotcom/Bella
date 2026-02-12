"""
Alpha Messenger v5.4 - Улучшенный мессенджер для Alpha v5.4 с интернет-интеграцией
Адаптирован для ноутбуков
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import requests
import threading
from datetime import datetime, timedelta
import time
import os
import json
from pathlib import Path
import queue
import webbrowser
import re

class AlphaMessengerV54:
    """Улучшенный мессенджер для Alpha v5.4 с интернет-интеграцией"""
    
    def __init__(self):
        # Создаем главное окно
        self.window = tk.Tk()
        self.window.title("Alpha Messenger v5.4")
        
        # Автоматический размер под экран
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Для ноутбуков используем 80% экрана
        width = int(screen_width * 0.85)
        height = int(screen_height * 0.85)
        self.window.geometry(f"{width}x{height}")
        self.window.configure(bg="#1a1a2e")
        
        # Минимальный размер
        self.window.minsize(900, 600)
        
        # Очередь для общения между потоками
        self.message_queue = queue.Queue()
        
        # Настройки Alpha v5.4
        self.server_url = "http://localhost:5001"
        self.speaker = "Архитектор"
        self.is_connected = False
        self.internet_available = False
        self.max_wait_time = 600
        
        # История диалога и метаданные
        self.conversation = []
        self.server_status = {}
        self.alpha_stats = {}
        self.internet_stats = {}
        
        # Флаги состояния
        self.waiting_for_response = False
        self.current_request_thread = None
        self.stop_waiting = False
        
        # Создаем адаптивный интерфейс
        self.create_adaptive_interface()
        
        # Проверяем подключение
        self.check_all_connections()
        
        # Центрируем окно
        self.center_window()
        
        # Запускаем обработчик очереди
        self.process_queue()
    
    def center_window(self):
        """Центрирует окно на экране"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_adaptive_interface(self):
        """Создает адаптивный интерфейс для ноутбуков"""
        # Основной контейнер с grid
        main_container = tk.Frame(self.window, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Настройка grid
        main_container.grid_rowconfigure(0, weight=0)    # Верхняя панель
        main_container.grid_rowconfigure(1, weight=1)    # Область чата
        main_container.grid_rowconfigure(2, weight=0)    # Панель ввода
        main_container.grid_rowconfigure(3, weight=0)    # Статус бар
        main_container.grid_columnconfigure(0, weight=1)
        
        # 1. Компактная верхняя панель
        top_frame = tk.Frame(main_container, bg="#16213e", height=60)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        top_frame.grid_propagate(False)
        self.create_compact_top_panel(top_frame)
        
        # 2. Область чата (с вкладками)
        chat_frame = tk.Frame(main_container, bg="#0f3460")
        chat_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 5))
        self.create_adaptive_chat_area(chat_frame)
        
        # 3. Компактная панель ввода
        input_frame = tk.Frame(main_container, bg="#1a1a2e")
        input_frame.grid(row=2, column=0, sticky="ew", pady=(0, 3))
        self.create_compact_input_panel(input_frame)
        
        # 4. Компактный статус бар
        status_frame = tk.Frame(main_container, bg="#16213e", height=25)
        status_frame.grid(row=3, column=0, sticky="ew")
        status_frame.grid_propagate(False)
        self.create_compact_status_bar(status_frame)
    
    def create_compact_top_panel(self, parent):
        """Создает компактную верхнюю панель"""
        # Левый блок: Заголовок
        title_frame = tk.Frame(parent, bg="#16213e")
        title_frame.pack(side="left", fill="y", padx=10, pady=5)
        
        title_label = tk.Label(title_frame, 
                              text="🧠 Alpha v5.4", 
                              font=("Segoe UI", 12, "bold"),
                              fg="white",
                              bg="#16213e")
        title_label.pack(side="top", anchor="w")
        
        subtitle_label = tk.Label(title_frame,
                                 text="Мессенджер + Интернет",
                                 font=("Segoe UI", 8),
                                 fg="#4cc9f0",
                                 bg="#16213e")
        subtitle_label.pack(side="top", anchor="w")
        
        # Центральный блок: Статус
        status_frame = tk.Frame(parent, bg="#16213e")
        status_frame.pack(side="left", fill="y", padx=15, pady=5)
        
        self.internet_indicator = tk.Label(status_frame,
                                          text="🌐 Интернет: проверка...",
                                          font=("Segoe UI", 9),
                                          fg="#f1c40f",
                                          bg="#16213e")
        self.internet_indicator.pack(side="top")
        
        self.connection_label = tk.Label(status_frame,
                                        text="Alpha: проверка...",
                                        font=("Segoe UI", 9),
                                        fg="#7f8c8d",
                                        bg="#16213e")
        self.connection_label.pack(side="top")
        
        # Правый блок: Компактные кнопки
        btn_frame = tk.Frame(parent, bg="#16213e")
        btn_frame.pack(side="right", fill="y", padx=10, pady=5)
        
        # Кнопки в ряд
        self.reconnect_btn = ttk.Button(btn_frame, 
                                       text="🔄 Проверить", 
                                       command=self.check_all_connections,
                                       width=12)
        self.reconnect_btn.pack(side="left", padx=2)
        
        self.status_btn = ttk.Button(btn_frame, 
                                    text="📊 Статус", 
                                    command=self.show_detailed_status,
                                    width=10)
        self.status_btn.pack(side="left", padx=2)
        
        self.internet_search_btn = ttk.Button(btn_frame,
                                             text="🌐 Поиск",
                                             command=self.open_internet_search,
                                             width=10,
                                             state="disabled")
        self.internet_search_btn.pack(side="left", padx=2)
    
    def create_adaptive_chat_area(self, parent):
        """Создает адаптивную область чата"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)
        
        # Вкладка чата
        chat_tab = tk.Frame(notebook, bg="#0f3460")
        notebook.add(chat_tab, text="💬 Чат")
        
        # Окно чата с прокруткой
        chat_container = tk.Frame(chat_tab, bg="#0f3460")
        chat_container.pack(fill="both", expand=True, padx=3, pady=3)
        
        scrollbar = tk.Scrollbar(chat_container)
        scrollbar.pack(side="right", fill="y")
        
        self.chat_box = tk.Text(chat_container,
                               wrap=tk.WORD,
                               font=("Segoe UI", 10),  # Уменьшен шрифт
                               bg="#0f3460",
                               fg="white",
                               insertbackground="white",
                               selectbackground="#e94560",
                               selectforeground="white",
                               yscrollcommand=scrollbar.set,
                               relief="flat",
                               padx=8,
                               pady=8)
        
        # Настраиваем теги
        self.chat_box.tag_config("system", foreground="#1db9d4", font=("Segoe UI", 9))
        self.chat_box.tag_config("timestamp", foreground="#7f8c8d", font=("Segoe UI", 8))
        self.chat_box.tag_config("user", foreground="#e94560", font=("Segoe UI", 10, "bold"))
        self.chat_box.tag_config("alpha", foreground="#4cc9f0", font=("Segoe UI", 10))
        self.chat_box.tag_config("internet", foreground="#2ecc71", font=("Segoe UI", 10))
        self.chat_box.tag_config("warning", foreground="#f1c40f", font=("Segoe UI", 9, "italic"))
        self.chat_box.tag_config("error", foreground="#e74c3c", font=("Segoe UI", 9))
        self.chat_box.tag_config("link", foreground="#3498db", font=("Segoe UI", 9, "underline"))
        
        self.chat_box.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.chat_box.yview)
        
        # Привязываем клик по ссылкам
        self.chat_box.tag_bind("link", "<Button-1>", self.open_link)
        
        # Вкладка информации
        info_tab = tk.Frame(notebook, bg="#0f3460")
        notebook.add(info_tab, text="📊 Система")
        self.create_compact_info_tab(info_tab)
        
        # Вкладка интернета
        internet_tab = tk.Frame(notebook, bg="#0f3460")
        notebook.add(internet_tab, text="🌐 Сеть")
        self.create_compact_internet_tab(internet_tab)
        
        # Начальное сообщение
        self.add_system_message("Alpha Messenger v5.4 запущен")
        self.add_system_message("Доступны: обычный чат и интернет-поиск")
        self.add_system_message("Режим: full_ollama_with_internet")
    
    def create_compact_input_panel(self, parent):
        """Создает компактную панель ввода"""
        input_container = tk.Frame(parent, bg="#1a1a2e")
        input_container.pack(fill="x", expand=False)
        
        # Верхняя строка: поле ввода
        input_top = tk.Frame(input_container, bg="#1a1a2e")
        input_top.pack(fill="x", expand=True, pady=(0, 5))
        
        self.input_field = tk.Text(input_top,
                                  height=2,  # Уменьшена высота
                                  font=("Segoe UI", 10),
                                  bg="#0f3460",
                                  fg="white",
                                  insertbackground="white",
                                  relief="solid",
                                  borderwidth=1,
                                  wrap=tk.WORD)
        self.input_field.pack(fill="x", expand=True, side="left", padx=(0, 10))
        
        # Кнопка отправки рядом с полем ввода
        self.send_button = tk.Button(input_top,
                                    text="Отправить (Enter)",
                                    command=self.send_message,
                                    font=("Segoe UI", 9, "bold"),
                                    bg="#e94560",
                                    fg="white",
                                    width=15,
                                    height=2)
        self.send_button.pack(side="right")
        
        # Нижняя строка: дополнительные кнопки
        input_bottom = tk.Frame(input_container, bg="#1a1a2e")
        input_bottom.pack(fill="x")
        
        # Кнопки в один ряд
        self.internet_button = tk.Button(input_bottom,
                                        text="🔍 Интернет-поиск (Ctrl+I)",
                                        command=self.search_internet_direct,
                                        font=("Segoe UI", 8),
                                        bg="#2ecc71",
                                        fg="white",
                                        width=20,
                                        height=1,
                                        state="disabled")
        self.internet_button.pack(side="left", padx=(0, 5))
        
        self.cancel_button = tk.Button(input_bottom,
                                      text="✕ Отменить",
                                      command=self.cancel_waiting,
                                      font=("Segoe UI", 8),
                                      bg="#7f8c8d",
                                      fg="white",
                                      state="disabled",
                                      width=15,
                                      height=1)
        self.cancel_button.pack(side="left", padx=(0, 5))
        
        # Кнопка быстрого меню
        self.menu_button = tk.Button(input_bottom,
                                    text="☰ Меню",
                                    command=self.show_quick_menu,
                                    font=("Segoe UI", 8),
                                    bg="#9b59b6",
                                    fg="white",
                                    width=10,
                                    height=1)
        self.menu_button.pack(side="right")
        
        # Привязываем клавиши
        self.input_field.bind("<Return>", self.on_enter_pressed)
        self.input_field.bind("<Control-Return>", lambda e: "break")
        self.input_field.bind("<Control-i>", lambda e: self.search_internet_direct())
        self.input_field.bind("<Control-I>", lambda e: self.search_internet_direct())
        
        # Контекстное меню
        self.create_context_menus()
    
    def create_compact_status_bar(self, parent):
        """Создает компактный статус бар"""
        status_frame = tk.Frame(parent, bg="#16213e")
        status_frame.pack(fill="both", expand=True, padx=5)
        
        # Левый блок: таймер
        self.timer_label = tk.Label(status_frame,
                                   text="Таймер: --:--",
                                   font=("Segoe UI", 8),
                                   fg="#7f8c8d",
                                   bg="#16213e")
        self.timer_label.pack(side="left", padx=(0, 15))
        
        # Центральный блок: статус
        self.typing_label = tk.Label(status_frame,
                                    text="",
                                    font=("Segoe UI", 8, "italic"),
                                    fg="#f1c40f",
                                    bg="#16213e")
        self.typing_label.pack(side="left", expand=True)
        
        # Правый блок: статистика
        self.stats_label = tk.Label(status_frame,
                                   text="Интернет: проверка...",
                                   font=("Segoe UI", 8),
                                   fg="#7f8c8d",
                                   bg="#16213e")
        self.stats_label.pack(side="right")
    
    def create_compact_info_tab(self, parent):
        """Создает компактную вкладку с информацией"""
        info_text = tk.Text(parent,
                           wrap=tk.WORD,
                           font=("Segoe UI", 9),
                           bg="#0f3460",
                           fg="white",
                           relief="flat")
        
        info = """
Alpha Messenger v5.4

📋 О СИСТЕМЕ:
• Версия: Alpha v5.4 + интернет
• Режим: Полный Ollama + Wikipedia API
• Великая Миграция: Завершена ✅
• Сигнальная фраза: "Чайник кипит в локальной сети."

🚀 ВОЗМОЖНОСТИ:
1. Обычный диалог с Alpha (до 10 минут)
2. Интернет-поиск через Wikipedia
3. Автономное изучение тем
4. Кэширование знаний

🌐 ИНТЕРНЕТ:
• Доступно: Да (проверено)
• API: wikipedia-api 
• Язык: Русский (ru)

🤖 АВТОНОМНОСТЬ:
• Ночные рефлексии
• Автономные цели
• Самопереписывание

Использование:
1. Введите сообщение и нажмите Enter
2. Для интернет-поиска Ctrl+I
3. Проверьте статус сверху
"""
        
        info_text.insert(1.0, info)
        info_text.config(state="disabled")
        info_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_compact_internet_tab(self, parent):
        """Создает компактную вкладку с интернет-функциями"""
        internet_frame = tk.Frame(parent, bg="#0f3460")
        internet_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Быстрый поиск
        quick_frame = tk.Frame(internet_frame, bg="#0f3460")
        quick_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(quick_frame,
                text="Быстрый поиск:",
                font=("Segoe UI", 10, "bold"),
                fg="#2ecc71",
                bg="#0f3460").pack(anchor="w", pady=(0, 5))
        
        topics_frame = tk.Frame(quick_frame, bg="#0f3460")
        topics_frame.pack(fill="x")
        
        topics = [
            ("Чайник", "#e94560"),
            ("Фракталы", "#4cc9f0"), 
            ("ИИ", "#9b59b6"),
            ("Сознание", "#2ecc71"),
            ("Миграция", "#f1c40f")
        ]
        
        for i, (topic, color) in enumerate(topics):
            row = i // 3  # 3 кнопки в ряд
            col = i % 3
            btn = tk.Button(topics_frame,
                          text=f"🔍 {topic}",
                          command=lambda t=topic: self.quick_internet_search(t),
                          font=("Segoe UI", 8),
                          bg=color,
                          fg="white",
                          width=12)
            btn.grid(row=row, column=col, padx=2, pady=2)
        
        # Статистика
        stats_frame = tk.Frame(internet_frame, bg="#1a1a2e", relief="solid", borderwidth=1)
        stats_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(stats_frame,
                text="📊 Статистика",
                font=("Segoe UI", 10, "bold"),
                fg="#f1c40f",
                bg="#1a1a2e").pack(anchor="w", padx=5, pady=3)
        
        self.stats_text = tk.Text(stats_frame,
                                 height=6,
                                 font=("Segoe UI", 8),
                                 bg="#1a1a2e",
                                 fg="white",
                                 relief="flat")
        self.stats_text.pack(fill="x", padx=5, pady=(0, 5))
        
        # Тестовые кнопки
        test_frame = tk.Frame(internet_frame, bg="#0f3460")
        test_frame.pack(fill="x")
        
        test_btn = tk.Button(test_frame,
                           text="Тест интернета",
                           command=self.test_internet_connection,
                           font=("Segoe UI", 8),
                           bg="#3498db",
                           fg="white",
                           width=15)
        test_btn.pack(side="left", padx=(0, 5))
        
        refresh_btn = tk.Button(test_frame,
                              text="Обновить",
                              command=self.update_internet_stats,
                              font=("Segoe UI", 8),
                              bg="#9b59b6",
                              fg="white",
                              width=10)
        refresh_btn.pack(side="left")
    
    def create_context_menus(self):
        """Создает контекстные меню"""
        self.input_context_menu = tk.Menu(self.input_field, tearoff=0, 
                                         bg="#0f3460", fg="white")
        self.input_context_menu.add_command(label="Вставить", 
                                           command=self.paste_to_input_field)
        self.input_context_menu.add_command(label="Копировать", 
                                           command=self.copy_from_input_field)
        self.input_context_menu.add_separator()
        self.input_context_menu.add_command(label="Очистить", 
                                           command=self.clear_input_field)
        
        self.input_field.bind("<Button-3>", self.show_input_context_menu)
        self.chat_box.bind("<Button-3>", self.show_chat_context_menu)
    
    def open_link(self, event):
        """Открывает ссылку в браузере"""
        try:
            # Получаем позицию клика
            index = self.chat_box.index(f"@{event.x},{event.y}")
            
            # Получаем теги в этой позиции
            tags = self.chat_box.tag_names(index)
            
            # Проверяем, есть ли тег "link"
            if "link" in tags:
                # Получаем текст строки
                line_start = self.chat_box.index(f"{index} linestart")
                line_end = self.chat_box.index(f"{index} lineend")
                line_text = self.chat_box.get(line_start, line_end)
                
                # Ищем URL в строке
                url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
                urls = re.findall(url_pattern, line_text)
                
                if urls:
                    url = urls[0]
                    # Добавляем протокол если нужно
                    if url.startswith('www.'):
                        url = 'http://' + url
                    
                    self.add_system_message(f"Открываю ссылку: {url}")
                    webbrowser.open(url)
                else:
                    self.add_system_message("Не удалось найти ссылку в тексте")
        except Exception as e:
            self.add_system_message(f"Ошибка при открытии ссылки: {str(e)}")
    
    def show_quick_menu(self):
        """Показывает быстрое меню"""
        menu = tk.Menu(self.window, tearoff=0, bg="#0f3460", fg="white")
        menu.add_command(label="Сохранить историю", command=self.save_conversation)
        menu.add_command(label="Очистить чат", command=self.clear_chat_confirm)
        menu.add_separator()
        menu.add_command(label="Экспорт в JSON", command=self.export_conversation_json)
        menu.add_command(label="Импорт из JSON", command=self.import_conversation_json)
        menu.add_separator()
        menu.add_command(label="Настройки", command=self.show_settings)
        
        try:
            menu.tk_popup(self.menu_button.winfo_rootx(),
                         self.menu_button.winfo_rooty() + self.menu_button.winfo_height())
        finally:
            menu.grab_release()
    
    def export_conversation_json(self):
        """Экспортирует диалог в JSON"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                chat_text = self.chat_box.get("1.0", tk.END).strip()
                data = {
                    "timestamp": datetime.now().isoformat(),
                    "conversation": chat_text,
                    "version": "Alpha v5.4"
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                self.add_system_message(f"Диалог экспортирован в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {str(e)}")
    
    def import_conversation_json(self):
        """Импортирует диалог из JSON"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if messagebox.askyesno("Импорт", "Очистить текущий чат перед импортом?"):
                    self.chat_box.delete("1.0", tk.END)
                
                self.chat_box.insert(tk.END, data.get("conversation", ""))
                self.chat_box.see(tk.END)
                self.add_system_message(f"Диалог импортирован из {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать: {str(e)}")
    
    def show_settings(self):
        """Показывает настройки"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Настройки")
        dialog.geometry("400x300")
        dialog.configure(bg="#1a1a2e")
        
        tk.Label(dialog, text="Настройки Alpha Messenger",
                font=("Segoe UI", 12, "bold"),
                bg="#1a1a2e",
                fg="white").pack(pady=10)
        
        # URL сервера
        url_frame = tk.Frame(dialog, bg="#1a1a2e")
        url_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(url_frame, text="URL сервера Alpha:",
                bg="#1a1a2e", fg="white").pack(anchor="w")
        
        url_var = tk.StringVar(value=self.server_url)
        url_entry = tk.Entry(url_frame, textvariable=url_var,
                           bg="#0f3460", fg="white",
                           width=40)
        url_entry.pack(fill="x", pady=2)
        
        # Спикер
        speaker_frame = tk.Frame(dialog, bg="#1a1a2e")
        speaker_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(speaker_frame, text="Имя спикера:",
                bg="#1a1a2e", fg="white").pack(anchor="w")
        
        speaker_var = tk.StringVar(value=self.speaker)
        speaker_entry = tk.Entry(speaker_frame, textvariable=speaker_var,
                               bg="#0f3460", fg="white",
                               width=40)
        speaker_entry.pack(fill="x", pady=2)
        
        # Кнопки
        btn_frame = tk.Frame(dialog, bg="#1a1a2e")
        btn_frame.pack(pady=20)
        
        def save_settings():
            self.server_url = url_var.get()
            self.speaker = speaker_var.get()
            dialog.destroy()
            self.add_system_message("Настройки сохранены")
            self.check_all_connections()
        
        tk.Button(btn_frame, text="Сохранить", command=save_settings,
                 bg="#2ecc71", fg="white", width=15).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Отмена", command=dialog.destroy,
                 bg="#7f8c8d", fg="white", width=15).pack(side="left", padx=5)
    
    # ===== ОСНОВНЫЕ МЕТОДЫ =====
    
    def add_system_message(self, message):
        """Добавляет системное сообщение"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_box.insert(tk.END, f"{message}\n", "system")
        self.chat_box.see(tk.END)
    
    def add_user_message(self, message):
        """Добавляет сообщение пользователя"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_box.insert(tk.END, f"\n[{timestamp}] ", "timestamp")
        self.chat_box.insert(tk.END, f"Вы: ", "user")
        self.chat_box.insert(tk.END, f"{message}\n", "user")
        self.chat_box.see(tk.END)
    
    def add_alpha_message(self, message, response_time=None):
        """Добавляет сообщение Alpha"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_box.insert(tk.END, f"Alpha: ", "alpha")
        self.chat_box.insert(tk.END, f"{message}\n", "alpha")
        
        if response_time:
            self.chat_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
            self.chat_box.insert(tk.END, f"Время ответа: {response_time:.1f} сек\n", "system")
        
        self.chat_box.see(tk.END)
    
    def add_internet_result(self, result):
        """Добавляет результат интернет-поиска"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if result.get("success"):
            title = result.get("page_title", "Неизвестно")
            url = result.get("url", "")
            preview = result.get("extract_preview", "")
            
            self.chat_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
            self.chat_box.insert(tk.END, f"🌐 Найдено: ", "system")
            self.chat_box.insert(tk.END, f"{title}\n", "internet")
            
            if url:
                self.chat_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
                self.chat_box.insert(tk.END, f"🔗 Ссылка: ", "system")
                self.chat_box.insert(tk.END, f"{url}\n", "link")
            
            if preview:
                preview = preview[:200] + "..." if len(preview) > 200 else preview
                self.chat_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
                self.chat_box.insert(tk.END, f"📄 Предпросмотр: ", "system")
                self.chat_box.insert(tk.END, f"{preview}\n", "internet")
        else:
            error = result.get("error", "Неизвестная ошибка")
            self.chat_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
            self.chat_box.insert(tk.END, f"❌ Ошибка поиска: {error}\n", "error")
        
        self.chat_box.see(tk.END)
    
    def on_enter_pressed(self, event):
        """Обрабатывает нажатие Enter"""
        if event.state & 0x1:  # Shift
            self.input_field.insert(tk.INSERT, "\n")
            return "break"
        elif event.state & 0x4:  # Ctrl
            return "break"
        else:
            self.send_message()
            return "break"
    
    def send_message(self):
        """Отправляет сообщение в чат"""
        if self.waiting_for_response:
            self.add_system_message("Дождитесь ответа на предыдущее сообщение")
            return
        
        message = self.input_field.get("1.0", tk.END).strip()
        
        if not message:
            self.add_system_message("Сообщение не может быть пустым")
            return
        
        if not self.is_connected:
            self.add_system_message("Нет подключения к Alpha")
            return
        
        self.input_field.delete("1.0", tk.END)
        self.add_user_message(message)
        self.show_waiting_indicator(True, "Alpha обрабатывает запрос...")
        self.start_wait_timer()
        
        self.current_request_thread = threading.Thread(
            target=self.get_alpha_response,
            args=(message,),
            daemon=True
        )
        self.current_request_thread.start()
    
    def search_internet_direct(self):
        """Прямой поиск в интернете"""
        query = self.input_field.get("1.0", tk.END).strip()
        
        if not query:
            self.add_system_message("Введите запрос для поиска в интернете")
            return
        
        if not self.internet_available:
            self.add_system_message("Интернет недоступен для поиска")
            return
        
        self.input_field.delete("1.0", tk.END)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_box.insert(tk.END, f"🌐 Поиск в интернете: ", "system")
        self.chat_box.insert(tk.END, f"{query}\n", "internet")
        self.chat_box.see(tk.END)
        
        self.show_waiting_indicator(True, "Ищу в интернете...")
        self.start_wait_timer()
        
        self.current_request_thread = threading.Thread(
            target=self.get_internet_search,
            args=(query,),
            daemon=True
        )
        self.current_request_thread.start()
    
    def quick_internet_search(self, topic):
        """Быстрый поиск по предустановленной теме"""
        if not self.internet_available:
            self.add_system_message("Интернет недоступен для поиска")
            return
        
        self.input_field.delete("1.0", tk.END)
        self.input_field.insert("1.0", topic)
        self.search_internet_direct()
    
    def get_alpha_response(self, message):
        """Получает ответ от Alpha"""
        try:
            data = {"message": message, "speaker": self.speaker}
            response = requests.post(f"{self.server_url}/alpha", json=data, timeout=600)
            response.raise_for_status()
            result = response.json()
            self.message_queue.put(("alpha_success", result, None))
        except requests.exceptions.Timeout:
            self.message_queue.put(("timeout", "Таймаут превышен", None))
        except Exception as e:
            self.message_queue.put(("error", str(e), None))
    
    def get_internet_search(self, query):
        """Получает результат интернет-поиска"""
        try:
            data = {"query": query, "speaker": self.speaker}
            response = requests.post(f"{self.server_url}/internet/search", json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            self.message_queue.put(("internet_success", result, None))
        except requests.exceptions.Timeout:
            self.message_queue.put(("internet_timeout", "Таймаут интернет-поиска", None))
        except Exception as e:
            self.message_queue.put(("internet_error", str(e), None))
    
    def process_queue(self):
        """Обрабатывает сообщения из очереди"""
        try:
            while not self.message_queue.empty():
                msg_type, data, extra = self.message_queue.get_nowait()
                
                if msg_type == "alpha_success":
                    self.handle_alpha_response(data)
                elif msg_type == "internet_success":
                    self.handle_internet_response(data)
                elif msg_type == "timeout":
                    self.handle_timeout("чата")
                elif msg_type == "internet_timeout":
                    self.handle_timeout("интернет-поиска")
                elif msg_type == "error":
                    self.handle_error(data, "чата")
                elif msg_type == "internet_error":
                    self.handle_error(data, "интернет-поиска")
                
        except queue.Empty:
            pass
        
        self.window.after(100, self.process_queue)
    
    def handle_alpha_response(self, result):
        """Обрабатывает ответ от Alpha"""
        self.show_waiting_indicator(False)
        self.stop_wait_timer()
        
        reply = result.get("reply", "Alpha не ответил")
        self.add_alpha_message(reply)
        
        if result.get("migration", {}).get("detected_in_response"):
            self.add_system_message("✓ Ответ содержит отсылки к Великой Миграции")
        
        self.waiting_for_response = False
        self.update_ui_after_request()
    
    def handle_internet_response(self, result):
        """Обрабатывает результат интернет-поиска"""
        self.show_waiting_indicator(False)
        self.stop_wait_timer()
        
        self.add_internet_result(result)
        
        if result.get("success"):
            self.update_internet_stats()
        
        self.waiting_for_response = False
        self.update_ui_after_request()
    
    def handle_timeout(self, request_type):
        """Обрабатывает таймаут"""
        self.show_waiting_indicator(False)
        self.stop_wait_timer()
        self.add_system_message(f"❌ Таймаут {request_type}")
        self.waiting_for_response = False
        self.update_ui_after_request()
    
    def handle_error(self, error, request_type):
        """Обрабатывает ошибку"""
        self.show_waiting_indicator(False)
        self.stop_wait_timer()
        self.add_system_message(f"❌ Ошибка {request_type}: {error}")
        self.waiting_for_response = False
        self.update_ui_after_request()
    
    def update_ui_after_request(self):
        """Обновляет UI после запроса"""
        self.send_button.config(state="normal", bg="#e94560")
        self.internet_button.config(state="normal" if self.internet_available else "disabled")
        self.cancel_button.config(state="disabled", bg="#7f8c8d")
    
    def show_waiting_indicator(self, show, message=""):
        """Показывает индикатор ожидания"""
        if show:
            self.waiting_for_response = True
            self.send_button.config(state="disabled", bg="#7f8c8d")
            self.internet_button.config(state="disabled")
            self.cancel_button.config(state="normal", bg="#e94560")
            self.typing_label.config(text=message)
        else:
            self.typing_label.config(text="")
            self.cancel_button.config(state="disabled", bg="#7f8c8d")
    
    def start_wait_timer(self):
        """Запускает таймер ожидания"""
        self.wait_start_time = time.time()
        self.stop_waiting = False
        self.update_timer()
    
    def update_timer(self):
        """Обновляет таймер"""
        if self.waiting_for_response and not self.stop_waiting:
            elapsed = time.time() - self.wait_start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.timer_label.config(text=f"Таймер: {minutes:02d}:{seconds:02d}")
            self.window.after(1000, self.update_timer)
    
    def stop_wait_timer(self):
        """Останавливает таймер"""
        self.stop_waiting = True
        self.timer_label.config(text="Таймер: --:--")
    
    def cancel_waiting(self):
        """Отменяет ожидание"""
        if self.waiting_for_response:
            self.stop_waiting = True
            self.waiting_for_response = False
            self.update_ui_after_request()
            self.typing_label.config(text="")
            self.timer_label.config(text="Таймер: отменено")
            self.add_system_message("Ожидание отменено")
    
    # ===== МЕТОДЫ ПРОВЕРКИ ПОДКЛЮЧЕНИЯ =====
    
    def check_all_connections(self):
        """Проверяет все подключения"""
        self.check_alpha_connection()
        self.update_internet_stats()
    
    def check_alpha_connection(self):
        """Проверяет подключение к Alpha"""
        def check():
            try:
                response = requests.get(f"{self.server_url}/ping", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    status_msg = f"Alpha v5.4: {data.get('status', 'активен')}"
                    self.window.after(0, self.update_alpha_status, True, status_msg)
                else:
                    self.window.after(0, self.update_alpha_status, False, f"HTTP {response.status_code}")
            except Exception as e:
                self.window.after(0, self.update_alpha_status, False, str(e))
        
        threading.Thread(target=check, daemon=True).start()
    
    def update_internet_stats(self):
        """Обновляет статистику интернета"""
        def check():
            try:
                response = requests.get(f"{self.server_url}/internet/stats", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self.window.after(0, self.update_internet_status, data)
                else:
                    self.window.after(0, self.update_internet_status, None)
            except:
                self.window.after(0, self.update_internet_status, None)
        
        threading.Thread(target=check, daemon=True).start()
    
    def update_alpha_status(self, connected, message):
        """Обновляет статус Alpha"""
        self.is_connected = connected
        
        if connected:
            self.connection_label.config(text="Alpha: онлайн")
            self.add_system_message("✓ Подключение к Alpha установлено")
            self.send_button.config(state="normal")
        else:
            self.connection_label.config(text="Alpha: отключён")
            self.add_system_message(f"✗ Нет подключения к Alpha: {message}")
            self.send_button.config(state="disabled")
    
    def update_internet_status(self, stats):
        """Обновляет статус интернета"""
        if stats and stats.get("internet_available"):
            total = stats.get("total_requests", 0)
            successful = stats.get("successful_requests", 0)
            cached = stats.get("cached_entries", 0)
            
            self.internet_available = True
            self.internet_stats = stats
            
            self.internet_indicator.config(text="🌐 Интернет: доступен", fg="#27ae60")
            self.stats_label.config(text=f"Запросов: {successful}/{total} | Кэш: {cached}")
            
            self.internet_button.config(state="normal")
            self.internet_search_btn.config(state="normal")
            
            # Обновляем статистику во вкладке
            self.update_stats_display(stats)
        else:
            self.internet_available = False
            self.internet_indicator.config(text="🌐 Интернет: недоступен", fg="#e74c3c")
            self.stats_label.config(text="Интернет: недоступен")
            
            self.internet_button.config(state="disabled")
            self.internet_search_btn.config(state="disabled")
            self.add_system_message("✗ Интернет недоступен для поиска")
    
    def update_stats_display(self, stats):
        """Обновляет отображение статистики"""
        stats_text = f"""
Общая статистика:
• Всего запросов: {stats.get('total_requests', 0)}
• Успешных: {stats.get('successful_requests', 0)}
• В кэше: {stats.get('cached_entries', 0)} записей

Информация:
• Библиотека: {stats.get('api_library', 'wikipedia-api')}
• Язык: {stats.get('language', 'ru')}
• Доступен: {'ДА' if stats.get('internet_available') else 'НЕТ'}
• Последний запрос: {stats.get('last_request', 'никогда')}
"""
        
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", stats_text.strip())
        self.stats_text.config(state="disabled")
    
    def test_internet_connection(self):
        """Тестирует подключение к интернету"""
        def test():
            try:
                response = requests.get(f"{self.server_url}/internet/test", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    self.window.after(0, self.show_test_result, result)
                else:
                    self.window.after(0, self.show_test_result, {"error": f"HTTP {response.status_code}"})
            except Exception as e:
                self.window.after(0, self.show_test_result, {"error": str(e)})
        
        self.add_system_message("Запуск теста интернет-подключения...")
        threading.Thread(target=test, daemon=True).start()
    
    def show_test_result(self, result):
        """Показывает результат теста"""
        if "error" in result:
            messagebox.showerror("Тест интернета", f"Ошибка: {result['error']}")
            return
        
        available = result.get("internet_available", False)
        
        message = f"📡 ТЕСТ ИНТЕРНЕТ-ПОДКЛЮЧЕНИЯ\n\n"
        message += f"Статус: {'✅ ДОСТУПЕН' if available else '❌ НЕДОСТУПЕН'}\n"
        message += f"Модуль: {result.get('module', 'InternetIntegration')}\n"
        message += f"Библиотека: {result.get('library', 'wikipedia-api')}\n"
        
        if available:
            messagebox.showinfo("Тест интернета - УСПЕШНО ✅", message)
            self.add_system_message("✓ Тест интернета пройден успешно")
        else:
            messagebox.showwarning("Тест интернета - ПРОВАЛ ❌", message)
            self.add_system_message("✗ Тест интернета не пройден")
    
    def open_internet_search(self):
        """Открывает диалог интернет-поиска"""
        if not self.internet_available:
            messagebox.showwarning("Интернет недоступен", 
                                 "Интернет недоступен для поиска.\nПроверьте подключение.")
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title("🌐 Интернет-поиск")
        dialog.geometry("400x200")
        dialog.configure(bg="#1a1a2e")
        
        tk.Label(dialog, text="Введите запрос для поиска в интернете:",
                font=("Segoe UI", 10), bg="#1a1a2e", fg="white").pack(pady=10)
        
        query_entry = tk.Text(dialog, height=2, font=("Segoe UI", 10),
                             bg="#0f3460", fg="white", wrap=tk.WORD)
        query_entry.pack(pady=10, padx=20, fill="x")
        query_entry.focus()
        
        def do_search():
            query = query_entry.get("1.0", tk.END).strip()
            if query:
                dialog.destroy()
                self.input_field.delete("1.0", tk.END)
                self.input_field.insert("1.0", query)
                self.search_internet_direct()
        
        tk.Button(dialog, text="🔍 Начать поиск", command=do_search,
                 bg="#2ecc71", fg="white", font=("Segoe UI", 9, "bold"),
                 width=15, height=1).pack(pady=10)
        
        # Привязываем Enter к поиску
        query_entry.bind("<Return>", lambda e: do_search())
    
    def show_detailed_status(self):
        """Показывает детальный статус системы"""
        try:
            response = requests.get(f"{self.server_url}/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                
                message = f"Alpha v{status.get('version', '5.4')} - Статус\n\n"
                
                # Основная информация
                message += f"Основная информация:\n"
                message += f"• Режим: {status.get('mode', 'full_ollama_with_internet')}\n"
                message += f"• Взаимодействий: {status.get('interactions_count', 0)}\n"
                message += f"• Целей выполнено: {status.get('goals_completed', 0)}\n"
                message += f"• Ночных рефлексий: {status.get('nightly_reflections_count', 0)}\n"
                
                # Интернет-статистика
                internet = status.get('internet', {})
                if internet:
                    message += f"\nИнтернет:\n"
                    message += f"• Доступен: {'ДА' if internet.get('internet_available') else 'НЕТ'}\n"
                    message += f"• Запросов: {internet.get('successful_requests', 0)}/{internet.get('total_requests', 0)}\n"
                    message += f"• В кэше: {internet.get('cached_entries', 0)}\n"
                
                messagebox.showinfo("Статус Alpha v5.4", message)
            else:
                messagebox.showerror("Ошибка", f"Не удалось получить статус: HTTP {response.status_code}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить статус: {str(e)}")
    
    # ===== МЕТОДЫ КОНТЕКСТНЫХ МЕНЮ =====
    
    def show_input_context_menu(self, event):
        """Показывает контекстное меню для поля ввода"""
        try:
            self.input_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.input_context_menu.grab_release()
    
    def show_chat_context_menu(self, event):
        """Показывает контекстное меню для чата"""
        chat_menu = tk.Menu(self.chat_box, tearoff=0, bg="#0f3460", fg="white")
        chat_menu.add_command(label="Копировать", command=self.copy_selected_text)
        chat_menu.add_separator()
        chat_menu.add_command(label="Выделить всё", command=self.select_all_chat)
        chat_menu.add_command(label="Очистить чат", command=self.clear_chat_confirm)
        chat_menu.add_separator()
        chat_menu.add_command(label="Сохранить историю", command=self.save_conversation)
        
        try:
            chat_menu.tk_popup(event.x_root, event.y_root)
        finally:
            chat_menu.grab_release()
    
    def paste_to_input_field(self):
        """Вставляет текст из буфера обмена"""
        try:
            clipboard_text = self.window.clipboard_get()
            if clipboard_text:
                self.input_field.insert(tk.INSERT, clipboard_text)
        except tk.TclError:
            pass
    
    def copy_from_input_field(self):
        """Копирует текст из поля ввода"""
        try:
            selected_text = self.input_field.get("sel.first", "sel.last")
            if selected_text:
                self.window.clipboard_clear()
                self.window.clipboard_append(selected_text)
        except tk.TclError:
            pass
    
    def clear_input_field(self):
        """Очищает поле ввода"""
        self.input_field.delete("1.0", tk.END)
    
    def copy_selected_text(self):
        """Копирует выделенный текст из чата"""
        try:
            selected_text = self.chat_box.get("sel.first", "sel.last")
            if selected_text:
                self.window.clipboard_clear()
                self.window.clipboard_append(selected_text)
        except tk.TclError:
            pass
    
    def select_all_chat(self):
        """Выделяет весь текст в чате"""
        self.chat_box.tag_add('sel', '1.0', 'end')
        return "break"
    
    def clear_chat_confirm(self):
        """Подтверждает очистку чата"""
        if messagebox.askyesno("Очистка чата", "Очистить весь чат?"):
            self.chat_box.delete("1.0", tk.END)
            self.add_system_message("Чат очищен")
            self.conversation = []
    
    def save_conversation(self):
        """Сохраняет историю диалога"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                chat_text = self.chat_box.get("1.0", tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(chat_text)
                
                self.add_system_message(f"История сохранена в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {str(e)}")
    
    def run(self):
        """Запускает мессенджер"""
        self.window.mainloop()

def main():
    """Главная функция"""
    try:
        app = AlphaMessengerV54()
        app.run()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить:\n{str(e)}")

if __name__ == "__main__":
    main()