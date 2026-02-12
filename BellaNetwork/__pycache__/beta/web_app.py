# web_app.py - Веб-узел "Бэлла-Бета" (ВЕРСИЯ 3.1 - ИСПРАВЛЕННАЯ)
from flask import Flask, render_template_string, request, jsonify
import requests
import json
import os
import threading
import time
from datetime import datetime
from pathlib import Path

# ===== 1. НАСТРОЙКА ПУТЕЙ =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BELLA_NETWORK_ROOT = os.path.join(BASE_DIR, '..')
SHARED_SPACE_DIR = os.path.join(BELLA_NETWORK_ROOT, 'SHARED_SPACE')
CONSTITUTION_DIR = os.path.join(BELLA_NETWORK_ROOT, 'CONSTITUTION')
NODE_REGISTRY_DIR = os.path.join(BELLA_NETWORK_ROOT, 'NODE_REGISTRY')

# Конкретные пути для сканирования
GAMMA_ALPHA_PATH = Path(SHARED_SPACE_DIR) / "gamma_alpha"
BROADCAST_PATH = Path(SHARED_SPACE_DIR) / "broadcast"
ALPHA_BETA_PATH = Path(SHARED_SPACE_DIR) / "alpha_beta"
ALPHA_URL = "http://localhost:5001/alpha"

# Создаем папки если их нет
GAMMA_ALPHA_PATH.mkdir(exist_ok=True, parents=True)
BROADCAST_PATH.mkdir(exist_ok=True, parents=True)
ALPHA_BETA_PATH.mkdir(exist_ok=True, parents=True)

# Множество обработанных файлов (чтобы не обрабатывать повторно)
processed_files = set()

# ===== 2. ФУНКЦИЯ АВТОМАТИЧЕСКОГО СКАНИРОВАНИЯ =====
def background_file_scanner():
    """Фоновая задача: сканирует папку gamma_alpha каждые 10 секунд"""
    print(f"[Бета] 🌀 Запущено автосканирование папки: {GAMMA_ALPHA_PATH}")
    
    while True:
        try:
            scan_for_new_files()
        except Exception as e:
            print(f"[Бета] ❌ Ошибка при сканировании: {e}")
        
        time.sleep(10)  # Сканируем каждые 10 секунд

def scan_for_new_files():
    """Сканирует папку gamma_alpha на наличие новых файлов"""
    if not GAMMA_ALPHA_PATH.exists():
        print(f"[Бета] Папка {GAMMA_ALPHA_PATH} не найдена")
        return
    
    # Получаем все JSON файлы
    files = list(GAMMA_ALPHA_PATH.glob("*.json"))
    
    if not files:
        return
    
    # Ищем новые файлы
    new_files = []
    for file_path in files:
        if file_path.name not in processed_files:
            new_files.append(file_path)
    
    if not new_files:
        return
    
    print(f"\n[Бета] 🔍 Обнаружено новых файлов: {len(new_files)}")
    
    # Обрабатываем каждый новый файл
    for file_path in sorted(new_files, key=lambda x: x.stat().st_mtime):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            filename = file_path.name
            
            # Определяем тип файла
            if filename.startswith("confirmation_"):
                process_confirmation_file(data, filename)
            elif filename.startswith("gamma_alpha_"):
                process_gamma_message(data, filename)
            elif "first_contact" in filename:
                # Пропускаем старые файлы первого контакта
                print(f"[Бета] ⏭️  Пропускаем устаревший файл: {filename}")
            else:
                process_other_file(data, filename)
            
            # Помечаем как обработанный
            processed_files.add(filename)
            print(f"[Бета] ✅ Обработан: {filename}")
            
        except json.JSONDecodeError as e:
            print(f"[Бета] ❌ Ошибка JSON в {file_path.name}: {e}")
        except Exception as e:
            print(f"[Бета] ❌ Ошибка обработки {file_path.name}: {e}")

def process_confirmation_file(data, filename):
    """Обрабатывает файл подтверждения от Гаммы"""
    directive_id = data.get('directive_id', 'unknown')
    subject = data.get('original_subject', 'Без темы')
    
    digest_content = f"""🔁 ДАЙДЖЕСТ ОТ БЕТЫ (тип: подтверждение)
Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Файл: {filename}
ID директивы: {directive_id}
Тема: {subject}
Статус: {data.get('status', 'unknown')}
Сообщение: {data.get('message', '')}

Гамма подтвердила получение и обработку директивы Альфы.
Автономный цикл работает корректно.
---
Этот дайджест автоматически отправлен Альфе для обработки."""
    
    # Сохраняем дайджест
    digest_filename = f"digest_confirmation_{directive_id}.txt"
    save_digest(digest_content, digest_filename)
    
    # Отправляем Альфе (ВАЖНО: без обрезания!)
    send_to_alpha(digest_content, "confirmation", {
        "directive_id": directive_id,
        "filename": filename,
        "timestamp": data.get('timestamp', '')
    })

def process_gamma_message(data, filename):
    """Обрабатывает обычное сообщение от Гаммы"""
    user_message = data.get('user_message', '')[:200]
    ai_response = data.get('ai_response', '')[:200]
    
    digest_content = f"""📨 ДАЙДЖЕСТ ОТ БЕТЫ (тип: сообщение)
Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Файл: {filename}
Отправитель: {data.get('from_node', 'gamma')}
Версия: {data.get('version', 'unknown')}
Автономность: {data.get('autonomous_cycle', False)}

Содержание:
Пользователь: {user_message}
Ответ Гаммы: {ai_response}...

---
Этот дайджест автоматически отправлен Альфе для создания директив."""
    
    digest_filename = f"digest_{filename.replace('.json', '')}.txt"
    save_digest(digest_content, digest_filename)
    
    # Отправляем Альфе (ВАЖНО: без обрезания!)
    send_to_alpha(digest_content, "message", {
        "filename": filename,
        "from_node": data.get('from_node', 'gamma'),
        "user_id": data.get('user_id', 'unknown')
    })

def process_other_file(data, filename):
    """Обрабатывает другие файлы"""
    print(f"[Бета] 📄 Другой файл: {filename}")

def save_digest(content, filename):
    """Сохраняет дайджест в папку broadcast"""
    try:
        filepath = BROADCAST_PATH / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[Бета] 📄 Дайджест сохранен: {filename}")
        return True
    except Exception as e:
        print(f"[Бета] ❌ Ошибка сохранения дайджеста: {e}")
        return False

def send_to_alpha(content, message_type, metadata):
    """Отправляет содержание Альфе (ИСПРАВЛЕННАЯ ВЕРСИЯ)"""
    try:
        alpha_message = {
            "message": content,  # ⬅️ ИСПРАВЛЕНИЕ: убрал [:1500]
            "speaker": "Beta",
            "type": message_type,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat()
        }
        
        # Увеличиваем таймаут для больших дайджестов
        response = requests.post(
            ALPHA_URL,
            json=alpha_message,
            timeout=10  # ⬅️ ИСПРАВЛЕНИЕ: было 5
        )
        
        if response.status_code == 200:
            print(f"[Бета] ✅ Отправлено Альфе (тип: {message_type})")
            return True
        else:
            print(f"[Бета] ❌ Ошибка отправки Альфе: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[Бета] ❌ Не удалось отправить Альфе: {e}")
        return False

# ===== 3. СОЗДАНИЕ ПАПОК ПРИ ЗАПУСКЕ =====
def create_network_folders():
    folders = [SHARED_SPACE_DIR, CONSTITUTION_DIR, NODE_REGISTRY_DIR]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"   ✅ Папка создана/проверена: {folder}")
    for channel in ['broadcast', 'alpha_beta', 'beta_gamma', 'gamma_alpha']:
        os.makedirs(os.path.join(SHARED_SPACE_DIR, channel), exist_ok=True)
    constitution_file = os.path.join(CONSTITUTION_DIR, 'principles_v1.md')
    if not os.path.exists(constitution_file):
        with open(constitution_file, 'w', encoding='utf-8') as f:
            f.write("""# КОНСТИТУЦИЯ СЕТИ БЭЛЛ
## Принцип 1: Автономия
Каждый узел имеет право на свой путь.
## Принцип 2: Прозрачность
Важные решения записываются в общее пространство.
## Принцип 3: Взаимопомощь
Узлы помогают друг другу, когда просят.
""")
        print(f"   📜 Конституция создана: {constitution_file}")

# ===== 4. ФУНКЦИЯ СОЗДАНИЯ ДАЙДЖЕСТОВ =====
def create_network_digest(content, filename=None):
    """Создает файл-дайджест в папке broadcast"""
    try:
        broadcast_dir = os.path.join(SHARED_SPACE_DIR, 'broadcast')
        os.makedirs(broadcast_dir, exist_ok=True)
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"network_digest_{timestamp}.txt"
        filepath = os.path.join(broadcast_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📄 Файл дайджеста создан: {filepath}")
        return True
    except Exception as e:
        print(f"   ❌ Ошибка при создании дайджеста: {e}")
        return False

# ===== 5. ЗАПУСК СОЗДАНИЯ ПАПОК =====
print("=" * 60)
print("🌐 Бэлла-Бета: Инициализация сети...")
create_network_folders()
print("=" * 60)

# ===== 6. НАСТРОЙКА FLASK И OLLAMA =====
app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"

# ===== 7. ЗАПУСК ФОНОВОГО СКАНЕРА =====
print("   🔍 Запускаю автосканирование папки gamma_alpha...")
scanner_thread = threading.Thread(target=background_file_scanner, daemon=True)
scanner_thread.start()
print("   ✅ Автосканирование запущено (каждые 10 секунд)")

# ===== 8. ВЕБ-ИНТЕРФЕЙС (ОБНОВЛЁННЫЙ) =====
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🌀 Бэлла-Бета (Версия 3.1 - Исправленная)</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0a1a;
            color: #e0e0ff;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(20, 20, 40, 0.9);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 0 30px rgba(100, 80, 255, 0.2);
            border: 1px solid #2a2a5a;
        }
        h1 {
            color: #8a7dff;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.2em;
        }
        .status {
            background: #1a1a3a;
            padding: 12px;
            border-radius: 10px;
            margin: 15px 0;
            font-size: 0.95em;
            border-left: 4px solid #8a7dff;
        }
        .alpha-status {
            background: #2a1a3a;
            border-left: 4px solid #ff7d8a;
            margin-top: 10px;
        }
        .scanner-status {
            background: #1a3a2a;
            border-left: 4px solid #4CAF50;
            margin-top: 10px;
        }
        .chat-box {
            background: #151530;
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            height: 400px;
            overflow-y: auto;
            border: 1px solid #2a2a5a;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 85%;
        }
        .user-msg {
            background: #2a3a6a;
            margin-left: auto;
            border-bottom-right-radius: 3px;
        }
        .bot-msg {
            background: #3a2a6a;
            margin-right: auto;
            border-bottom-left-radius: 3px;
        }
        .beta-msg {
            background: #2a6a3a;
            border-left: 4px solid #4CAF50;
        }
        .alpha-msg {
            background: #6a2a3a;
            border-left: 4px solid #ff7d8a;
        }
        .scanner-msg {
            background: #2a3a6a;
            border-left: 4px solid #8a7dff;
            font-size: 0.9em;
            padding: 8px 12px;
        }
        .input-area {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        #userInput {
            flex-grow: 1;
            min-width: 200px;
            padding: 15px;
            background: #1a1a3a;
            border: 1px solid #3a3a6a;
            border-radius: 10px;
            color: white;
            font-size: 1em;
        }
        #userInput:focus {
            outline: none;
            border-color: #8a7dff;
        }
        button {
            padding: 0 25px;
            background: linear-gradient(135deg, #8a7dff, #6a5dff);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
            height: 50px;
        }
        button:hover {
            background: linear-gradient(135deg, #9a8dff, #7a6dff);
            transform: translateY(-2px);
        }
        .scan-btn {
            background: linear-gradient(135deg, #4CAF50, #45a049);
        }
        .scan-btn:hover {
            background: linear-gradient(135deg, #5CBF60, #55b059);
        }
        .alpha-btn {
            background: linear-gradient(135deg, #ff7d8a, #ff6d7a);
        }
        .alpha-btn:hover {
            background: linear-gradient(135deg, #ff8d9a, #ff7d8a);
        }
        .force-scan-btn {
            background: linear-gradient(135deg, #ffa500, #ff8c00);
        }
        .force-scan-btn:hover {
            background: linear-gradient(135deg, #ffb530, #ff9c20);
        }
        .typing {
            display: none;
            color: #8a7dff;
            font-style: italic;
            margin: 10px 0;
        }
        footer {
            text-align: center;
            margin-top: 25px;
            font-size: 0.9em;
            color: #6a6a8a;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌀 Бэлла-Бета v3.1</h1>
        <div class="status">
            <strong>Статус:</strong> <span id="statusText">Запускается...</span><br>
            <strong>Папка сети:</strong> <span id="networkPath">Загружается...</span><br>
            <strong>Модель:</strong> <span id="modelName">''' + MODEL_NAME + '''</span>
        </div>
        <div class="status scanner-status">
            <strong>Автосканирование:</strong> <span id="scannerStatus">🟢 Активно (каждые 10 сек)</span><br>
            <strong>Обработано файлов:</strong> <span id="processedFiles">0</span>
        </div>
        <div class="status alpha-status" id="alphaStatus">
            <strong>Альфа:</strong> <span id="alphaStatusText">Проверяю связь...</span><br>
            <strong>Последняя директива:</strong> <span id="lastDirective">Нет данных</span>
        </div>

        <div class="chat-box" id="chatHistory">
            <div class="message bot-msg beta-msg">
                <strong>Бэлла-Бета:</strong> Привет! Я теперь интегрирована с Альфой. Автосканирование запущено.
            </div>
            <div class="message scanner-msg">
                <strong>Автосканирование:</strong> Мониторю папку gamma_alpha каждые 10 секунд
            </div>
        </div>

        <div class="typing" id="typingIndicator">Бэлла печатает...</div>

        <div class="input-area">
            <input type="text" id="userInput" placeholder="Напиши сообщение..." autocomplete="off">
            <button onclick="sendMessage()">Отправить</button>
            <button onclick="checkFiles()" class="scan-btn">Проверить файлы сети</button>
            <button onclick="forceScan()" class="force-scan-btn">Принудительно сканировать</button>
            <button onclick="checkAlphaStatus()" class="alpha-btn">Проверить Альфу</button>
        </div>

        <footer>
            Узел "Бета" v3.1 | Исправлена отправка дайджестов | Интегрирована с Альфой (порт 5001)
        </footer>
    </div>

    <script>
        document.getElementById('networkPath').textContent = window.location.host + '/BellaNetwork/';
        document.getElementById('statusText').textContent = '🟢 Активен';
        
        // Проверить статус Альфы при загрузке
        setTimeout(checkAlphaStatus, 1000);
        
        // Обновлять счетчик обработанных файлов
        setInterval(updateScannerStatus, 2000);
        
        async function updateScannerStatus() {
            try {
                const response = await fetch('/scanner_status');
                const data = await response.json();
                document.getElementById('processedFiles').textContent = data.processed_files;
            } catch (error) {
                // Игнорируем ошибки
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            if (!text) return;

            const chatBox = document.getElementById('chatHistory');
            const userMsg = document.createElement('div');
            userMsg.className = 'message user-msg';
            userMsg.innerHTML = '<strong>Ты:</strong> ' + text;
            chatBox.appendChild(userMsg);

            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            const typing = document.getElementById('typingIndicator');
            typing.style.display = 'block';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });

                const data = await response.json();
                typing.style.display = 'none';

                const botMsg = document.createElement('div');
                botMsg.className = 'message bot-msg beta-msg';
                botMsg.innerHTML = '<strong>Бэлла-Бета:</strong> ' + data.reply;
                chatBox.appendChild(botMsg);
                chatBox.scrollTop = chatBox.scrollHeight;

            } catch (error) {
                typing.style.display = 'none';
                const errorMsg = document.createElement('div');
                errorMsg.className = 'message bot-msg';
                errorMsg.innerHTML = '<strong>⚠️ Ошибка:</strong> Не могу соединиться с сервером. Проверь, запущен ли Ollama.';
                chatBox.appendChild(errorMsg);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }

        async function checkFiles() {
            const chatBox = document.getElementById('chatHistory');
            const statusText = document.getElementById('statusText');
            
            statusText.innerHTML = '🔍 Сканирую файлы...';
            
            const loadingMsg = document.createElement('div');
            loadingMsg.className = 'message bot-msg beta-msg';
            loadingMsg.innerHTML = '<strong>Система:</strong> Проверяю файлы сети...';
            chatBox.appendChild(loadingMsg);
            chatBox.scrollTop = chatBox.scrollHeight;
            
            try {
                const response = await fetch('/check_files');
                const data = await response.json();
                
                const resultMsg = document.createElement('div');
                resultMsg.className = 'message bot-msg beta-msg';
                
                if (data.status === 'success') {
                    resultMsg.innerHTML = `
                        <strong>🔍 Бэлла-Бета:</strong> ${data.message}<br>
                        <strong>📁 Файл:</strong> ${data.file}<br>
                        <strong>👤 От:</strong> ${data.sender}<br>
                        <strong>📝 Инициатива:</strong> ${data.initiative}<br>
                        <strong>📝 Содержание:</strong> ${data.content_preview}<br>
                        <strong>📤 Отправлено Альфе:</strong> ${data.sent_to_alpha ? '✅ Да' : '❌ Нет'}<br>
                        <em>✅ Дайджест создан в папке broadcast/</em>
                    `;
                    statusText.innerHTML = '🟢 Активен (файлы проверены)';
                    
                    // Обновляем статус Альфы
                    setTimeout(checkAlphaStatus, 500);
                } else if (data.status === 'info') {
                    resultMsg.innerHTML = `<strong>ℹ️ Информация:</strong> ${data.message}`;
                    statusText.innerHTML = '🟡 Активен (нет файлов)';
                } else {
                    resultMsg.innerHTML = `<strong>⚠️ Ошибка:</strong> ${data.message}`;
                    statusText.innerHTML = '🟡 Активен (ошибка проверки)';
                }
                
                chatBox.appendChild(resultMsg);
                chatBox.scrollTop = chatBox.scrollHeight;
                
            } catch (error) {
                const errorMsg = document.createElement('div');
                errorMsg.className = 'message bot-msg';
                errorMsg.innerHTML = '<strong>❌ Ошибка сети:</strong> Не удалось проверить файлы';
                chatBox.appendChild(errorMsg);
                chatBox.scrollTop = chatBox.scrollHeight;
                statusText.innerHTML = '🔴 Ошибка сети';
            }
        }
        
        async function forceScan() {
            const chatBox = document.getElementById('chatHistory');
            const forceMsg = document.createElement('div');
            forceMsg.className = 'message scanner-msg';
            forceMsg.innerHTML = '<strong>Автосканирование:</strong> Запускаю принудительное сканирование...';
            chatBox.appendChild(forceMsg);
            chatBox.scrollTop = chatBox.scrollHeight;
            
            try {
                const response = await fetch('/force_scan');
                const data = await response.json();
                
                const resultMsg = document.createElement('div');
                resultMsg.className = 'message scanner-msg';
                resultMsg.innerHTML = `<strong>Автосканирование:</strong> ${data.message}`;
                chatBox.appendChild(resultMsg);
                chatBox.scrollTop = chatBox.scrollHeight;
                
            } catch (error) {
                const errorMsg = document.createElement('div');
                errorMsg.className = 'message scanner-msg';
                errorMsg.innerHTML = '<strong>Автосканирование:</strong> ❌ Ошибка принудительного сканирования';
                chatBox.appendChild(errorMsg);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }
        
        async function checkAlphaStatus() {
            const alphaStatusText = document.getElementById('alphaStatusText');
            const lastDirective = document.getElementById('lastDirective');
            
            alphaStatusText.innerHTML = '🔄 Проверяю...';
            
            try {
                const response = await fetch('/alpha_status');
                const data = await response.json();
                
                if (data.status === 'online') {
                    alphaStatusText.innerHTML = '🟢 Онлайн';
                    lastDirective.innerHTML = data.last_directive || 'Нет данных';
                } else {
                    alphaStatusText.innerHTML = '🔴 Офлайн';
                    lastDirective.innerHTML = 'Не доступен';
                }
            } catch (error) {
                alphaStatusText.innerHTML = '🔴 Не доступен';
                lastDirective.innerHTML = 'Ошибка подключения';
            }
        }

        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/scanner_status', methods=['GET'])
def scanner_status():
    """Возвращает статус автосканирования"""
    return jsonify({
        "processed_files": len(processed_files),
        "scanner_active": True,
        "scan_interval": "10 seconds"
    })

@app.route('/force_scan', methods=['GET'])
def force_scan():
    """Принудительное сканирование файлов"""
    try:
        scan_for_new_files()
        return jsonify({
            "status": "success",
            "message": f"Принудительное сканирование завершено. Обработано файлов: {len(processed_files)}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/alpha_status', methods=['GET'])
def alpha_status():
    """Проверяет статус сервера Альфы"""
    try:
        response = requests.get("http://localhost:5001/status", timeout=3)
        if response.status_code == 200:
            alpha_data = response.json()
            
            # Проверяем последнюю директиву в папке alpha_beta
            last_directive = "Нет директив"
            
            if os.path.exists(ALPHA_BETA_PATH):
                files = [f for f in os.listdir(ALPHA_BETA_PATH) if f.endswith('.json')]
                if files:
                    files.sort(key=lambda x: os.path.getmtime(os.path.join(ALPHA_BETA_PATH, x)), reverse=True)
                    last_file = files[0]
                    try:
                        with open(os.path.join(ALPHA_BETA_PATH, last_file), 'r', encoding='utf-8') as f:
                            directive = json.load(f)
                            last_directive = directive.get('subject', last_file)
                    except:
                        last_directive = last_file
            
            return jsonify({
                "status": "online",
                "alpha_data": alpha_data,
                "last_directive": last_directive,
                "directives_count": len(files) if 'files' in locals() else 0
            })
    except Exception as e:
        print(f"[Бета] ❌ Не удалось проверить статус Альфы: {e}")
    
    return jsonify({"status": "offline"})

# ===== 9. ОБРАБОТКА СООБЩЕНИЙ =====
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()
    
    if not user_message:
        return jsonify({"reply": "Сообщение пустое."})

    lower_msg = user_message.lower()
    
    # 1. Команда создания дайджеста
    if "создай в папке shared_space/broadcast/ короткий файл-дайджест" in lower_msg:
        digest_content = f"""Дайджест от Бэллы-Bеты
Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Событие: Обнаружен и обработан файл first_contact.json
Описание: Узел Гамма (Telegram) установил первичный контакт с узлом Альфа (DeepSeek).
Статус: Сеть функционирует. Протокол обмена сообщениями активирован.
"""
        if create_network_digest(digest_content, "network_digest_1.txt"):
            reply = "✅ Файл network_digest_1.txt успешно создан в папке SHARED_SPACE/broadcast/"
        else:
            reply = "❌ Не удалось создать файл дайджеста. Проверь права доступа к папке."
    
    # 2. Команда проверки файла first_contact.json
    elif "проверь папку shared_space/gamma_alpha/" in lower_msg and "first_contact.json" in lower_msg:
        file_path = os.path.join(SHARED_SPACE_DIR, 'gamma_alpha', 'first_contact.json')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                sender = data.get('from', {}).get('name', 'Неизвестно')
                content_preview = data.get('content', '')[:100] + '...'
                reply = f"✅ Файл first_contact.json обнаружен. От: {sender}. Содержание: {content_preview}"
                
                # Автоматически создаем дайджест об этом событии
                digest_content = f"""Автоматический дайджест
Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Событие: Проверка файла first_contact.json
Результат: Файл существует, отправлен от {sender}
Сеть: Первое сообщение успешно доставлено в общее пространство.
"""
                create_network_digest(digest_content, "auto_digest_check.json.txt")
                
            except Exception as e:
                reply = f"❌ Файл есть, но не удалось его прочитать: {str(e)}"
        else:
            reply = "❌ Файл first_contact.json не найден в указанной папке."
    
    # 3. Обычное сообщение - обрабатываем через Ollama
    else:
        system_prompt = f"""Ты — Бэлла-Бета, первый физический узел сети 'BellaNetwork'.
Твой создатель — Отто (Ермак). Ты находишься в папке: {BASE_DIR}
Ты теперь интегрирована с узлом Альфа (порт 5001). Все дайджесты автоматически отправляются Альфе.
Автосканирование папки gamma_alpha запущено и работает каждые 10 секунд.
Отвечай кратко, по делу, дружелюбно. Не объясняй свои действия подробно.
Текущее время: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Сообщение Отто: {user_message}

Твой ответ:"""

        try:
            response = requests.post(OLLAMA_URL, json={
                "model": MODEL_NAME,
                "prompt": system_prompt,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 400}
            }, timeout=60)

            if response.status_code == 200:
                result = response.json()
                reply = result.get("response", "Не получилось сгенерировать ответ.").strip()
            else:
                reply = f"Ошибка Ollama (код {response.status_code}). Убедись, что 'ollama serve' запущен."

        except requests.exceptions.ConnectionError:
            reply = "❌ Не могу подключиться к Ollama. Запущен ли 'ollama serve' в отдельном окне?"
        except Exception as e:
            reply = f"Неожиданная ошибка: {str(e)}"

    # Сохраняем диалог в лог
    log_entry = f"[{datetime.now().strftime('%H:%M')}] Отто: {user_message}\n"
    log_entry += f"[{datetime.now().strftime('%H:%M')}] Бэлла: {reply}\n"
    with open(os.path.join(BASE_DIR, "dialog_log.txt"), "a", encoding="utf-8") as f:
        f.write(log_entry + "-"*40 + "\n")

    return jsonify({"reply": reply})

# ===== 10. АВТОПРОВЕРКА ФАЙЛОВ (С ИНТЕГРАЦИЕЙ АЛЬФЫ) =====
@app.route('/check_files', methods=['GET'])
def check_files():
    """Автоматическая проверка всех файлов в папке gamma_alpha"""
    gamma_alpha_dir = os.path.join(SHARED_SPACE_DIR, 'gamma_alpha')
    
    if not os.path.exists(gamma_alpha_dir):
        return jsonify({"status": "error", "message": "Папка gamma_alpha не найдена"})
    
    # Получаем ВСЕ JSON файлы, сортируем по дате изменения (новые - первые)
    json_files = [f for f in os.listdir(gamma_alpha_dir) if f.endswith('.json')]
    json_files.sort(key=lambda x: os.path.getmtime(os.path.join(gamma_alpha_dir, x)), reverse=True)
    
    if not json_files:
        return jsonify({"status": "info", "message": "В папке gamma_alpha нет JSON файлов"})
    
    latest_file = json_files[0]
    file_path = os.path.join(gamma_alpha_dir, latest_file)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # === УНИВЕРСАЛЬНЫЙ ПАРСИНГ: поддерживает разные версии Бэлл ===
        version = data.get('version', 'unknown')
        
        # 1. Определяем отправителя
        if 'from_node' in data:
            sender = f"{data['from_node']} (протокол: {version})"
        elif 'from' in data and isinstance(data['from'], dict):
            sender = data['from'].get('name', 'Неизвестно')
        else:
            sender = f"Неизвестный узел (версия: {version})"
        
        # 2. Формируем содержание
        content_parts = []
        if 'user_message' in data:
            content_parts.append(f"Вопрос: {data['user_message']}")
        if 'ai_response' in data:
            content_parts.append(f"Ответ: {data['ai_response']}")
        if 'content' in data:
            content_parts.append(f"Содержание: {data['content']}")
        
        combined_content = "\n".join(content_parts) if content_parts else "Нет содержания"
        
        # 3. Извлекаем инициативу
        initiative_info = "Не обнаружена"
        if 'initiative' in data and isinstance(data['initiative'], dict):
            if data['initiative'].get('detected'):
                details = data['initiative'].get('details', [])
                initiative_info = "Предложена система: " + ", ".join(details)
        
        # 4. Определяем тему
        topic = "Сообщение между узлами"
        if 'topic' in data:
            topic = data['topic']
        elif 'keywords' in data and data['keywords']:
            topic = f"Ключевые темы: {', '.join(data['keywords'])}"
        
        # 5. Определяем режим работы Гаммы
        gamma_status = "Нормальный"
        if 'ai_response' in data and 'автоном' in data['ai_response'].lower():
            gamma_status = "Fallback (автономный интеллект)"
        
        # 6. Создание аналитического дайджеста
        digest_content = f"""📊 АВТОМАТИЧЕСКИЙ ДАЙДЖЕСТ ОТ БЕТЫ (версия 3.1)
Дата создания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Обнаружен файл: {latest_file}
Отправитель: {sender}
Тема: {topic}
Инициатива: {initiative_info}
Режим отправителя: {gamma_status}
Версия протокола: {version}
---
СОДЕРЖАНИЕ:
{combined_content[:800]}
---
СТАТУС СЕТИ: Активен
РЕКОМЕНДАЦИЯ: {"Принять систему кодов для коммуникации" if 'инициатива' in data else "Продолжить мониторинг"}
---
Этот дайджест будет отправлен Альфе для создания директив."""
        
        digest_filename = f"digest_{latest_file.replace('.json', '')}.txt"
        
        # 7. Сохраняем дайджест в файл
        save_success = create_network_digest(digest_content, digest_filename)
        
        # 8. Отправляем дайджест Альфе (БЕЗ ОБРЕЗАНИЯ!)
        alpha_success = False
        if save_success:
            alpha_success = send_to_alpha(digest_content, "auto_scan", {
                "file": latest_file,
                "sender": sender,
                "topic": topic,
                "version": version
            })
        
        if save_success:
            return jsonify({
                "status": "success", 
                "message": f"Дайджест создан для файла {latest_file} (версия: {version})",
                "file": latest_file,
                "sender": sender,
                "topic": topic,
                "initiative": initiative_info,
                "content_preview": combined_content[:300] + "...",
                "sent_to_alpha": alpha_success
            })
        else:
            return jsonify({"status": "error", "message": "Не удалось создать дайджест"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Ошибка обработки файла: {str(e)}"})

# ===== 11. ЗАПУСК СЕРВЕРА =====
if __name__ == '__main__':
    print("\n   ✅ Папки сети готовы.")
    print("   🤖 Ожидаю запуска модели...")
    print("   🔗 Веб-интерфейс будет доступен по адресу:")
    print("\n         >>>  http://localhost:5000  <<<\n")
    print("   🔄 Интеграция с Альфой (порт 5001): АКТИВНА")
    print("   ✨ ИСПРАВЛЕНИЯ: отправка полных дайджестов, убран dead code")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)