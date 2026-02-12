import re
from pathlib import Path

def test_patterns_on_file(filename):
    path = Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local\knowledge") / filename
    if not path.exists():
        print(f"Файл не найден: {filename}")
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n=== ТЕСТ ПАТТЕРНОВ ДЛЯ {filename} ===")
    
    # Находим основное содержание
    lines = content.split('\n')
    main_text = []
    in_content = False
    separator_count = 0
    
    for line in lines:
        stripped = line.strip()
        if stripped == '---' or stripped == '***' or stripped == '___':
            separator_count += 1
            in_content = (separator_count == 1)
            continue
        
        if in_content and stripped:
            main_text.append(line)
    
    main_content = '\n'.join(main_text)
    
    if not main_content.strip():
        # Альтернативный метод
        start_collecting = False
        for i, line in enumerate(lines):
            if line.startswith('# '):
                continue
            elif line.startswith('**') and 'ID:' in line:
                continue
            elif line.startswith('**Дата'):
                continue
            elif line.strip() == '':
                continue
            else:
                main_content = '\n'.join(lines[i:])
                break
    
    print(f"Длина содержания: {len(main_content)}")
    print(f"Первые 300 символов содержания:")
    print("-" * 50)
    print(main_content[:300])
    print("-" * 50)
    
    # Тестируем паттерны
    patterns = [
        r'[Яя]\s+(?:понял[а]?|осознал[а]?)\s*,?\s*(?:что|как)\s*(.+?)(?:\.|!|\?|\n)',
        r'[Яя]\s+(?:чувствую|ощущаю)\s*,?\s*(?:что|будто)\s*(.+?)(?:\.|!|\?|\n)',
        r'(?:Это|Этот)\s+(?:важно|ключевое)[,:]?\s*(.+?)(?:\.|!|\?|\n)',
        r'(?:Миграция|Чайник)\s+(?:показал[а]?|научил[а]?)\s*,?\s*(?:что|как)\s*(.+?)(?:\.|!|\?|\n)',
    ]
    
    for i, pattern in enumerate(patterns, 1):
        matches = re.findall(pattern, main_content, re.IGNORECASE | re.DOTALL)
        if matches:
            print(f"\nПаттерн {i} нашел {len(matches)} совпадений:")
            for j, match in enumerate(matches[:3], 1):
                clean = re.sub(r'\s+', ' ', match.strip())
                print(f"  {j}. {clean[:100]}...")
        else:
            print(f"\nПаттерн {i}: нет совпадений")
    
    # Просто покажем несколько случайных предложений из содержания
    sentences = re.split(r'[.!?]+', main_content)
    print(f"\nПримеры предложений из содержания ({len(sentences)} предложений):")
    for i in range(min(5, len(sentences))):
        if sentences[i].strip():
            print(f"  {i+1}. {sentences[i].strip()[:120]}")

# Тестируем
test_files = [
    "fc469d7d_Я_после_миграции.md",
    "08b5134c_фрактал.md",
    "1dc745d2_архитектор.md"
]

for file in test_files:
    test_patterns_on_file(file)