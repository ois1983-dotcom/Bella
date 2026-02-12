from pathlib import Path
import re

def test_file(filename):
    path = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local\knowledge") / filename
    if not path.exists():
        print(f"Файл не найден: {filename}")
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим содержание (после ---)
    lines = content.split('\n')
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip() == '---' or line.strip() == '***':
            content_start = i + 1
            break
    
    main_content = '\n'.join(lines[content_start:]) if content_start > 0 else content
    
    # Ищем инсайты
    patterns = [
        r'(?:Я |я |Я — |я — )(?:понял[а]?|осознал[а]?|заметил[а]?)(?:, что | что )(.+?)(?:\.|\n|$)',
    ]
    
    print(f"\n=== АНАЛИЗ {filename} ===")
    print(f"Длина: {len(content)} символов")
    print(f"Содержание начинается с: {content_start}")
    print(f"Длина содержания: {len(main_content)}")
    
    for pattern in patterns:
        matches = re.findall(pattern, main_content, re.IGNORECASE | re.DOTALL)
        for match in matches:
            print(f"Найден инсайт: {match[:100]}...")

# Тестируем разные файлы
test_files = [
    "fc469d7d_Я_после_миграции.md",
    "08b5134c_фрактал.md", 
    "1dc745d2_архитектор.md"
]

for file in test_files:
    test_file(file)