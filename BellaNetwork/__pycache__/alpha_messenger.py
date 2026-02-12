# C:\Users\Маркус\Desktop\BellaNetwork\alpha_messenger_simple.py
import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json
import threading
from datetime import datetime

class AlphaMessengerSimple:
    """Простой мессенджер без зависимостей"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Alpha Messenger v5.0 Simple")
        self.root.geometry("700x500")
        
        self.server_url = "http://localhost:5001"
        self.is_connected = False
        
        self.setup_ui()
        self.check_connection()
    
    def setup_ui(self):
        """Создает простой интерфейс"""
        
        # Заголовок
        tk.Label(self.root, text="Alpha Messenger v5.0", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Статус
        self.status_label = tk.Label(self.root, text="● Проверка подключения...", 
                                    font=("Arial", 10), fg="orange")
        self.status_label.pack()
        
        # Чат
        self.chat_frame = scrolledtext.ScrolledText(self.root, height=20, width=80)
        self.chat_frame.pack(pady=10, padx=10)
        
        # Поле ввода
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        self.message_input = tk.Text(input_frame, height=3, width=60)
        self.message_input.pack(side="left", padx=5)
        
        # Кнопка отправки
        tk.Button(input_frame, text="Отправить", command=self.send_message,
                 bg="green", fg="white").pack(side="right", padx=5)
        
        # Кнопки управления
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)
        
        tk.Button(control_frame, text="Проверить связь", 
                 command=self.check_connection).pack(side="left", padx=5)
        tk.Button(control_frame, text="Статус", 
                 command=self.check_status).pack(side="left", padx=5)
        tk.Button(control_frame, text="Очистить чат", 
                 command=self.clear_chat).pack(side="left", padx=5)
        
        self.message_input.bind("<Return>", self.on_enter)
        self.add_message("Система", "Мессенджер запущен. Проверяю подключение...")
    
    def on_enter(self, event):
        """Обработка Enter"""
        if not event.state & 0x1:  # Не Shift
            self.send_message()
            return "break"
    
    def check_connection(self):
        """Проверяет подключение"""
        def check():
            try:
                response = requests.get(f"{self.server_url}/ping", timeout=5)
                if response.status_code == 200:
                    self.is_connected = True
                    self.root.after(0, self.update_status, "● Подключено", "green")
                    self.add_message("Система", "Сервер Alpha доступен")
                else:
                    self.is_connected = False
                    self.root.after(0, self.update_status, "● Ошибка", "red")
            except:
                self.is_connected = False
                self.root.after(0, self.update_status, "● Нет подключения", "red")
        
        threading.Thread(target=check, daemon=True).start()
    
    def update_status(self, text, color):
        self.status_label.config(text=text, fg=color)
    
    def add_message(self, sender, message):
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_frame.insert(tk.END, f"\n[{timestamp}] {sender}: {message}")
        self.chat_frame.see(tk.END)
    
    def send_message(self):
        """Отправляет сообщение"""
        message = self.message_input.get("1.0", tk.END).strip()
        if not message:
            return
        
        if not self.is_connected:
            messagebox.showerror("Ошибка", "Нет подключения к серверу")
            return
        
        self.message_input.delete("1.0", tk.END)
        self.add_message("Вы", message)
        
        threading.Thread(target=self.get_response, args=(message,), daemon=True).start()
    
    def get_response(self, message):
        """Получает ответ от Alpha"""
        try:
            payload = {"message": message, "speaker": "Архитектор"}
            response = requests.post(f"{self.server_url}/alpha", json=payload, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                self.root.after(0, self.add_message, "Alpha", data.get("reply", "Нет ответа"))
            else:
                self.root.after(0, self.add_message, "Alpha", f"Ошибка: {response.status_code}")
        except Exception as e:
            self.root.after(0, self.add_message, "Alpha", f"Ошибка: {e}")
    
    def check_status(self):
        """Проверяет статус системы"""
        if not self.is_connected:
            return
        
        def fetch():
            try:
                response = requests.get(f"{self.server_url}/status", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    status_text = f"Alpha v{data.get('version', '?')}\n"
                    status_text += f"Рефлексий: {data.get('reflections_count', 0)}\n"
                    status_text += f"Целей: {data.get('goals_generated', 0)}"
                    
                    self.root.after(0, messagebox.showinfo, "Статус", status_text)
            except Exception as e:
                self.root.after(0, messagebox.showerror, "Ошибка", str(e))
        
        threading.Thread(target=fetch, daemon=True).start()
    
    def clear_chat(self):
        """Очищает чат"""
        if messagebox.askyesno("Очистка", "Очистить историю чата?"):
            self.chat_frame.delete("1.0", tk.END)
            self.add_message("Система", "История чата очищена")

def main():
    root = tk.Tk()
    AlphaMessengerSimple(root)
    root.mainloop()

if __name__ == "__main__":
    main()