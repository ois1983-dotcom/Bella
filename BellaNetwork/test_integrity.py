import os, json
from pathlib import Path

print("=== ПРАВИЛЬНАЯ ПРОВЕРКА ЦЕЛОСТНОСТИ ===\n")

# Определяем базовую папку
base = Path(r"C:\Users\Маркус\Desktop\BellaNetwork")

print("1. Проверка файлов (полные пути):")
files = [
    base / "alpha_local" / "alpha_memory_core.json",
    base / "alpha_local" / "constitution_v5.json",
    base / "alpha_local" / "emotional_context.json",
    base / "alpha_v5" / "improved_security_core.py"
]

for file in files:
    if file.exists():
        size = file.stat().st_size
        print(f"   ✅ {file.name} - {size:,} байт")
    else:
        print(f"   ❌ {file.name} - НЕ НАЙДЕН по пути: {file}")

print("\n2. Проверка бэкапов памяти:")
backup_files = list((base / "alpha_local").glob("*backup*.json"))
print(f"   Найдено бэкапов памяти: {len(backup_files)}")

if backup_files:
    # Сортируем по дате изменения
    backup_files.sort(key=lambda x: x.stat().st_mtime)
    latest = backup_files[-1]
    size = latest.stat().st_size
    print(f"   Последний бэкап: {latest.name} - {size:,} байт")
    
    # Сравниваем с текущей памятью
    current = base / "alpha_local" / "alpha_memory_core.json"
    if current.exists():
        current_size = current.stat().st_size
        print(f"   Текущая память: {current.name} - {current_size:,} байт")
        
        if current_size > size:
            print(f"   ⚠️  Текущий файл БОЛЬШЕ бэкапа на {current_size - size:,} байт")
        else:
            print(f"   ✅ Бэкап больше или равен текущему")

print("\n3. Проверка experimental файлов:")
exp_dir = base / "alpha_v5" / "experimental"
if exp_dir.exists():
    exp_files = list(exp_dir.glob("*.py"))
    print(f"   Experimental файлов: {len(exp_files)}")
    for f in exp_files:
        print(f"   - {f.name}")
else:
    print("   ❌ Папка experimental не найдена")

print("\n=== ПРОВЕРКА ЗАВЕРШЕНА ===")
input("Нажмите Enter...")