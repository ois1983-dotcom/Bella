from memory_consolidation import MemoryConsolidatorV2
from pathlib import Path

consolidator = MemoryConsolidatorV2(
    Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local\knowledge"),
    Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local\alpha_memory_core.json")
)

result = consolidator.consolidate()
print(f"Обработано новых файлов: {result['new_files_processed']}")
print(f"Всего выводов в БД: {result['total_insights']}")

with open(Path(r"C:\Users\Маркус\Desktop\BellaNetwork\alpha_local\consolidation_summary.txt"), 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"\nСводка ({len(content)} символов):")
    print("-" * 50)
    print(content[:800])
    print("-" * 50)

consolidator.close()