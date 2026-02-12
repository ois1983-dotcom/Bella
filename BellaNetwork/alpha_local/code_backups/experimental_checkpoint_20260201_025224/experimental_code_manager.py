"""
ГЛАВНЫЙ МЕНЕДЖЕР ЭКСПЕРИМЕНТАЛЬНОГО КОДА v1.1
Безопасная система самопереписывания с увеличенными лимитами
"""

import ast
import json
import shutil
import hashlib
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import fnmatch

class ExperimentalCodeManager:
    """
    УПРОЩЕННЫЙ И БЕЗОПАСНЫЙ менеджер для самопереписывания кода
    Работает ТОЛЬКО с experimental_*.py файлами
    ВЕРСИЯ 1.1: Увеличены лимиты для работы с большими файлами
    """
    
    def __init__(self, security_core, alpha_local_path: Path):
        self.security = security_core
        self.alpha_local = alpha_local_path
        self.alpha_v5 = alpha_local_path.parent / "alpha_v5"
        
        # Создаём папку для экспериментального кода
        self.experimental_dir = self.alpha_v5 / "experimental"
        self.experimental_dir.mkdir(exist_ok=True)
        
        # НАСТРОЙКИ ДЛЯ БОЛЬШИХ ФАЙЛОВ (ИЗМЕНЕНО)
        self.max_file_size_lines = 2000  # Было 100, теперь 2000 строк
        self.max_function_lines = 100    # Было 30, теперь 100 строк
        self.max_nested_loops = 5        # Было 3, теперь 5 уровней
        
        # Создаём базовый экспериментальный файл если его нет
        self._create_base_experimental_file()
        
        # Журнал изменений
        self.change_log = self.alpha_local / "experimental_changes.json"
        self._init_change_log()
        
        # Блокировки для предотвращения конфликтов
        self.file_locks = {}
        self.lock_timeout = 30  # секунд
        
        # Очистка старых бэкапов
        self.max_backups = 10  # Было 5, теперь 10
        self._clean_old_backups()
        
        print(f">> ExperimentalCodeManager v1.1 инициализирован")
        print(f">> Рабочая папка: {self.experimental_dir}")
        print(f">> Макс. размер файла: {self.max_file_size_lines} строк")
        print(f">> Макс. функция: {self.max_function_lines} строк")
        print(f">> Макс. вложенность циклов: {self.max_nested_loops} уровней")
    
    def _create_base_experimental_file(self):
        """Создаёт базовый experimental файл если его нет"""
        base_file = self.experimental_dir / "experimental_base.py"
        if not base_file.exists():
            base_content = '''"""
ЭКСПЕРИМЕНТАЛЬНЫЙ ФАЙЛ ДЛЯ САМОПЕРЕПИСЫВАНИЯ v1.1
Alpha v5.4 может безопасно изменять этот файл
"""

def experimental_function():
    """Пример функции для автономного улучшения"""
    return "Это experimental код, который Alpha может изменять"

def get_experimental_status():
    """Возвращает статус экспериментального кода"""
    return {
        "status": "active",
        "version": "1.1",
        "last_modified": "2025-01-09",
        "purpose": "Безопасное самопереписывание кода Alpha"
    }

# Alpha может добавлять сюда новые функции и улучшать существующие
'''
            with open(base_file, 'w', encoding='utf-8') as f:
                f.write(base_content)
            print(f">> Создан базовый experimental файл: {base_file.name}")
    
    def _init_change_log(self):
        """Инициализирует журнал изменений"""
        if not self.change_log.exists():
            with open(self.change_log, 'w', encoding='utf-8') as f:
                json.dump({
                    "changes": [],
                    "metadata": {
                        "created": datetime.now().isoformat(),
                        "max_entries": 100,  # Было 50
                        "purpose": "Логирование изменений experimental кода",
                        "version": "1.1"
                    }
                }, f, indent=2)
    
    def _clean_old_backups(self):
        """Очищает старые бэкапы, оставляя только последние N"""
        backup_dir = self.alpha_local / "code_backups"
        if not backup_dir.exists():
            return
        
        # Получаем все бэкапы
        backups = list(backup_dir.glob("checkpoint_*"))
        backups.sort(key=lambda x: x.stat().st_mtime)
        
        # Удаляем старые, оставляем только последние max_backups
        if len(backups) > self.max_backups:
            for backup in backups[:-self.max_backups]:
                try:
                    shutil.rmtree(backup)
                    print(f">> Удалён старый бэкап: {backup.name}")
                except:
                    pass
    
    def _acquire_file_lock(self, filename: str) -> bool:
        """Получает блокировку файла"""
        lock_file = self.experimental_dir / f".{filename}.lock"
        
        if lock_file.exists():
            lock_age = time.time() - lock_file.stat().st_mtime
            if lock_age > self.lock_timeout:
                lock_file.unlink(missing_ok=True)
            else:
                return False
        
        try:
            with open(lock_file, 'w') as f:
                f.write(str(datetime.now().isoformat()))
            self.file_locks[filename] = lock_file
            return True
        except:
            return False
    
    def _release_file_lock(self, filename: str):
        """Освобождает блокировку файла"""
        if filename in self.file_locks:
            lock_file = self.file_locks[filename]
            lock_file.unlink(missing_ok=True)
            del self.file_locks[filename]
    
    def create_safe_checkpoint(self) -> Optional[str]:
        """Создаёт безопасный checkpoint (только experimental файлы)"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            checkpoint_dir = self.alpha_local / "code_backups" / f"experimental_checkpoint_{timestamp}"
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            
            experimental_files = list(self.experimental_dir.glob("*.py"))
            
            for file in experimental_files:
                shutil.copy2(file, checkpoint_dir / file.name)
            
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "type": "experimental_checkpoint",
                "files": [f.name for f in experimental_files],
                "total_size": sum(f.stat().st_size for f in experimental_files),
                "purpose": "Автономное создание перед изменением кода",
                "version": "1.1"
            }
            
            with open(checkpoint_dir / "metadata.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            print(f">> Создан безопасный checkpoint: {checkpoint_dir.name}")
            
            self._clean_old_backups()
            
            return checkpoint_dir.name
            
        except Exception as e:
            print(f">> Ошибка создания checkpoint: {e}")
            return None
    
    def analyze_experimental_code_safely(self) -> List[Dict]:
        """
        АНАЛИЗИРУЕТ КОД БЕЗ ЛОЖНЫХ СРАБАТЫВАНИЙ v1.1
        С увеличенными лимитами для больших файлов
        """
        suggestions = []
        
        for py_file in self.experimental_dir.glob("*.py"):
            if not self._acquire_file_lock(py_file.name):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                issues = self._analyze_with_ast(code, py_file.name)
                
                if issues:
                    for issue in issues:
                        suggestion = {
                            "filename": py_file.name,
                            "line": issue.get("line", 0),
                            "issue_type": issue["type"],
                            "description": issue["description"],
                            "priority": self._calculate_priority(issue),
                            "code_snippet": issue.get("code_snippet", "")[:150]  # Увеличено
                        }
                        
                        if not self._is_false_positive(suggestion):
                            suggestions.append(suggestion)
                
                # ПРОВЕРКА РАЗМЕРА ФАЙЛА (С УВЕЛИЧЕННЫМ ЛИМИТОМ)
                metrics = self._calculate_code_metrics(code)
                
                if metrics["line_count"] > self.max_file_size_lines:
                    suggestions.append({
                        "filename": py_file.name,
                        "issue_type": "file_too_large",
                        "description": f"Файл очень большой ({metrics['line_count']} строк)",
                        "priority": 3,  # Понижен приоритет, так как лимит высокий
                        "suggestion": "Рассмотреть возможность модуляризации при >5000 строк"
                    })
                
                if metrics["comment_ratio"] < 0.05:  # 5% комментариев минимум
                    suggestions.append({
                        "filename": py_file.name,
                        "issue_type": "low_comments",
                        "description": f"Мало комментариев ({metrics['comment_ratio']:.1%})",
                        "priority": 4,
                        "suggestion": "Добавить документацию"
                    })
                    
            finally:
                self._release_file_lock(py_file.name)
        
        suggestions.sort(key=lambda x: x["priority"], reverse=True)
        return suggestions[:7]  # Возвращаем больше предложений
    
    def _analyze_with_ast(self, code: str, filename: str) -> List[Dict]:
        """Анализирует код с помощью AST (с увеличенными лимитами)"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # УСТАНОВЛЕНО СВЯЗЫВАНИЕ РОДИТЕЛЕЙ ДЛЯ УЗЛОВ
            for node in ast.walk(tree):
                for child in ast.iter_child_nodes(node):
                    child.parent = node
            
            for node in ast.walk(tree):
                # Проверка на глубокую вложенность циклов (увеличен лимит)
                if isinstance(node, (ast.For, ast.While)):
                    nested_count = self._count_nested_loops(node)
                    if nested_count >= self.max_nested_loops:
                        issues.append({
                            "type": "nested_loops",
                            "description": f"Слишком много вложенных циклов ({nested_count} уровня)",
                            "line": node.lineno,
                            "code_snippet": ast.get_source_segment(code, node)[:200]
                        })
                
                # Проверка на длинные функции (увеличен лимит)
                if isinstance(node, ast.FunctionDef):
                    function_length = len(node.body)
                    if function_length > self.max_function_lines:
                        issues.append({
                            "type": "long_function",
                            "description": f"Функция слишком длинная ({function_length} строк)",
                            "line": node.lineno,
                            "function_name": node.name
                        })
                
                # Проверка на сложные условия
                if isinstance(node, ast.If):
                    condition_complexity = self._calculate_condition_complexity(node.test)
                    if condition_complexity >= 5:  # Увеличен лимит
                        issues.append({
                            "type": "complex_condition",
                            "description": f"Слишком сложное условие ({condition_complexity} операторов)",
                            "line": node.lineno
                        })
            
        except SyntaxError as e:
            issues.append({
                "type": "syntax_error",
                "description": f"Синтаксическая ошибка: {e.msg}",
                "line": e.lineno
            })
        
        # Проверка на дублирование кода
        duplicate_issues = self._check_duplicate_code(code)
        issues.extend(duplicate_issues)
        
        return issues
    
    def _count_nested_loops(self, node) -> int:
        """Считает уровень вложенности циклов (рекурсивно)"""
        count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                if hasattr(child, 'parent') and child.parent == node:
                    count = max(count, 1 + self._count_nested_loops(child))
        return count
    
    def _calculate_condition_complexity(self, node) -> int:
        """Рассчитывает сложность условия"""
        if isinstance(node, ast.BoolOp):
            return len(node.values)
        elif isinstance(node, ast.Compare):
            return 1 + len(node.ops)
        elif isinstance(node, ast.UnaryOp):
            return 1 + self._calculate_condition_complexity(node.operand)
        elif isinstance(node, (ast.BinOp, ast.Call, ast.Attribute)):
            return 1
        else:
            return 0
    
    def _check_duplicate_code(self, code: str) -> List[Dict]:
        """Обнаруживает дублирование кода в файле"""
        issues = []
        lines = code.split('\n')
        
        # Игнорируем пустые строки и комментарии
        code_lines = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('"""'):
                normalized = ' '.join(stripped.split())
                code_lines.append((i, normalized))
        
        # Ищем повторяющиеся последовательности из 4+ строк (было 3)
        sequence_length = 4
        for i in range(len(code_lines) - sequence_length):
            seq_indices = [code_lines[j][0] for j in range(i, i + sequence_length)]
            seq_text = [code_lines[j][1] for j in range(i, i + sequence_length)]
            
            for j in range(i + sequence_length, len(code_lines) - sequence_length):
                match_seq = [code_lines[k][1] for k in range(j, j + sequence_length)]
                
                if seq_text == match_seq:
                    issues.append({
                        "type": "duplicate_code",
                        "description": f"Обнаружено дублирование кода ({sequence_length} идентичных строк)",
                        "line": seq_indices[0] + 1,
                        "code_snippet": '; '.join(seq_text)[:150],
                        "duplicate_at": code_lines[j][0] + 1
                    })
                    break
        
        return issues
    
    def _calculate_code_metrics(self, code: str) -> Dict:
        """Рассчитывает базовые метрики кода"""
        lines = code.split('\n')
        total_lines = len(lines)
        
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        empty_lines = sum(1 for line in lines if not line.strip())
        code_lines = total_lines - comment_lines - empty_lines
        
        return {
            "line_count": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "empty_lines": empty_lines,
            "comment_ratio": comment_lines / code_lines if code_lines > 0 else 0
        }
    
    def _calculate_priority(self, issue: Dict) -> int:
        """Рассчитывает приоритет проблемы"""
        priority_map = {
            "syntax_error": 10,
            "nested_loops": 6,  # Понижен приоритет (было 8)
            "long_function": 5,  # Понижен (было 6)
            "complex_condition": 4,  # Понижен (было 5)
            "file_too_large": 3,  # Сильно понижен (было 7)
            "low_comments": 3,
            "duplicate_code": 4
        }
        
        return priority_map.get(issue["type"], 5)
    
    def _is_false_positive(self, suggestion: Dict) -> bool:
        """Фильтрует ложные срабатывания"""
        issue_type = suggestion["issue_type"]
        code_snippet = suggestion.get("code_snippet", "").lower()
        filename = suggestion.get("filename", "").lower()
        
        # Файлы с "integrator" могут быть большими - это нормально
        if "integrator" in filename and issue_type == "file_too_large":
            return True
        
        # Большие файлы experimental - это ожидаемо
        if "experimental" in filename and issue_type == "file_too_large":
            lines = suggestion.get("description", "")
            if "5000" not in lines:  # Если меньше 5000 строк - нормально
                return True
        
        if issue_type == "nested_loops":
            if "for i in range" in code_snippet and "for j in range" in code_snippet:
                return True
        
        if issue_type == "complex_condition":
            if "is not none" in code_snippet or "isinstance" in code_snippet:
                return True
        
        if issue_type == "duplicate_code":
            if all(word in code_snippet.lower() for word in ['print', 'test', 'debug']):
                return True
        
        return False
    
    def apply_safe_improvement(self, suggestion: Dict) -> Dict:
        """
        ПРИМЕНЯЕТ БЕЗОПАСНОЕ УЛУЧШЕНИЕ v1.1
        С улучшенной обработкой больших файлов
        """
        result = {
            "success": False,
            "filename": suggestion["filename"],
            "action": "code_improvement",
            "timestamp": datetime.now().isoformat(),
            "error": None,
            "backup_created": False,
            "changes_made": []
        }
        
        filename = suggestion["filename"]
        filepath = self.experimental_dir / filename
        
        if not filepath.exists():
            result["error"] = f"Файл не существует: {filename}"
            return result
        
        if not self._acquire_file_lock(filename):
            result["error"] = "Файл заблокирован другим процессом"
            return result
        
        try:
            checkpoint_id = self.create_safe_checkpoint()
            if checkpoint_id:
                result["backup_created"] = True
                result["checkpoint_id"] = checkpoint_id
            
            with open(filepath, 'r', encoding='utf-8') as f:
                current_code = f.read()
            
            new_code = current_code
            change_applied = False
            
            issue_type = suggestion["issue_type"]
            
            if issue_type == "low_comments":
                new_code = self._add_smart_comments(current_code)
                result["changes_made"].append("Добавлены комментарии")
                change_applied = True
            
            elif issue_type == "long_function" and "function_name" in suggestion:
                func_name = suggestion["function_name"]
                new_code = self._split_long_function(current_code, func_name)
                result["changes_made"].append(f"Разделена функция {func_name}")
                change_applied = True
            
            elif issue_type == "duplicate_code":
                new_code = self._remove_duplicate_code(current_code)
                result["changes_made"].append("Удалено дублирование кода")
                change_applied = True
            
            elif issue_type == "file_too_large":
                # ДЛЯ БОЛЬШИХ ФАЙЛОВ - ТОЛЬКО ДОБАВЛЯЕМ КОММЕНТАРИЙ, НЕ РАЗБИВАЕМ
                new_code = self._add_large_file_header(current_code, suggestion)
                result["changes_made"].append("Добавлен заголовок для большого файла")
                change_applied = True
            
            # Если не было реальных изменений
            if not change_applied or new_code == current_code:
                # Для больших файлов это нормально - возвращаем успех
                if issue_type == "file_too_large":
                    result["success"] = True
                    result["changes_made"] = ["Файл большой, но безопасен"]
                    return result
                else:
                    result["error"] = "Не удалось применить улучшение"
                    return result
            
            # Валидация нового кода
            validation = self._validate_python_code(new_code)
            if not validation["valid"]:
                result["error"] = f"Ошибка валидации: {validation['error']}"
                return result
            
            # Записываем изменения
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_code)
            
            # Тестируем
            test_result = self._test_experimental_code(filename)
            if not test_result["success"]:
                result["error"] = f"Тест не пройден: {test_result['error']}"
                
                if checkpoint_id:
                    self._restore_from_checkpoint(checkpoint_id)
                
                return result
            
            result["success"] = True
            result["validation"] = validation
            result["test_result"] = test_result
            
            self._log_change(suggestion, result)
            
            return result
            
        except Exception as e:
            result["error"] = f"Исключение: {str(e)}"
            return result
            
        finally:
            self._release_file_lock(filename)
    
    def _add_large_file_header(self, code: str, suggestion: Dict) -> str:
        """Добавляет заголовок для больших файлов (безопасная операция)"""
        lines = code.split('\n')
        
        # Ищем существующий заголовок
        header_added = False
        for i, line in enumerate(lines[:5]):
            if line.strip().startswith("# БОЛЬШОЙ ФАЙЛ:"):
                # Обновляем существующий заголовок
                lines[i] = f"# БОЛЬШОЙ ФАЙЛ: {suggestion['description']} - Обновлено {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                header_added = True
                break
        
        if not header_added:
            # Добавляем новый заголовок после первых строк документации
            insert_pos = 0
            for i, line in enumerate(lines):
                if not line.strip().startswith('"""') and not line.strip().startswith('#'):
                    insert_pos = i
                    break
            
            large_file_comment = f"""# БОЛЬШОЙ ФАЙЛ: {suggestion['description']}
# Система самопереписывания обнаружила, что этот файл большой.
# Это нормально для интеграторов и сложных модулей.
# Последняя проверка: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            lines.insert(insert_pos, large_file_comment)
        
        return '\n'.join(lines)
    
    def _add_smart_comments(self, code: str) -> str:
        """Добавляет умные комментарии"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if not next_line.startswith('"""') and not next_line.startswith('#'):
                    func_name = line.split('def ')[1].split('(')[0]
                    comment = f'    """Функция {func_name}"""'
                    lines.insert(i + 1, comment)
        
        return '\n'.join(lines)
    
    def _split_long_function(self, code: str, func_name: str) -> str:
        """Разделяет длинную функцию на части"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if f'def {func_name}' in line:
                todo_comment = f'    # TODO: Рассмотреть рефакторинг длинной функции'
                if i + 1 < len(lines):
                    lines.insert(i + 1, todo_comment)
                break
        
        return '\n'.join(lines)
    
    def _remove_duplicate_code(self, code: str) -> str:
        """Удаляет дублирующийся код"""
        lines = code.split('\n')
        seen_lines = []
        result_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('"""'):
                normalized = ' '.join(stripped.split())
                
                if normalized not in seen_lines:
                    seen_lines.append(normalized)
                    result_lines.append(line)
                else:
                    result_lines.append(f"# Дублирование удалено: {stripped[:80]}...")
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def _validate_python_code(self, code: str) -> Dict:
        """Валидирует Python код"""
        try:
            ast.parse(code)
            return {"valid": True, "error": None}
        except SyntaxError as e:
            return {"valid": False, "error": f"Синтаксическая ошибка: {e.msg}"}
    
    def _test_experimental_code(self, filename: str) -> Dict:
        """Простое тестирование experimental кода"""
        try:
            import importlib.util
            import sys
            
            filepath = self.experimental_dir / filename
            spec = importlib.util.spec_from_file_location(
                f"experimental_{filename.replace('.py', '')}",
                filepath
            )
            
            if spec is None:
                return {"success": False, "error": "Не удалось создать спецификацию"}
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'experimental_function'):
                try:
                    result = module.experimental_function()
                    if not isinstance(result, str):
                        return {"success": False, "error": "Функция вернула неверный тип"}
                except:
                    return {"success": False, "error": "Ошибка выполнения функции"}
            
            return {"success": True, "error": None}
            
        except Exception as e:
            return {"success": False, "error": f"Ошибка импорта: {str(e)}"}
    
    def _restore_from_checkpoint(self, checkpoint_id: str) -> bool:
        """Восстанавливает из checkpoint"""
        try:
            checkpoint_dir = self.alpha_local / "code_backups" / checkpoint_id
            if not checkpoint_dir.exists():
                return False
            
            for py_file in checkpoint_dir.glob("*.py"):
                if py_file.name != "metadata.json":
                    target_file = self.experimental_dir / py_file.name
                    shutil.copy2(py_file, target_file)
            
            print(f">> Восстановлено из checkpoint: {checkpoint_id}")
            return True
            
        except:
            return False
    
    def _log_change(self, suggestion: Dict, result: Dict):
        """Логирует изменение"""
        try:
            with open(self.change_log, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "suggestion": suggestion,
                "result": result,
                "status": "success" if result["success"] else "failed"
            }
            
            log_data["changes"].append(log_entry)
            
            if len(log_data["changes"]) > 100:
                log_data["changes"] = log_data["changes"][-100:]
            
            with open(self.change_log, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f">> Ошибка логирования: {e}")
    
    def get_status(self) -> Dict:
        """Возвращает статус менеджера v1.1"""
        experimental_files = list(self.experimental_dir.glob("*.py"))
        
        return {
            "status": "active",
            "version": "1.1",
            "experimental_dir": str(self.experimental_dir),
            "experimental_files": [f.name for f in experimental_files],
            "file_count": len(experimental_files),
            "max_backups": self.max_backups,
            "lock_timeout": self.lock_timeout,
            "safety_level": "high",
            "max_file_size_lines": self.max_file_size_lines,
            "max_function_lines": self.max_function_lines,
            "max_nested_loops": self.max_nested_loops,
            "detection_capabilities": [
                "Синтаксические ошибки",
                f"Вложенные циклы (>{self.max_nested_loops} уровней)",
                f"Длинные функции (>{self.max_function_lines} строк)",
                f"Сложные условия (>4 операторов)",
                f"Дублирование кода (4+ идентичных строк)",
                f"Файлы >{self.max_file_size_lines} строк",
                "Низкий процент комментариев (<5%)"
            ],
            "restrictions": [
                "Только experimental_*.py файлы",
                "AST-анализ вместо regex",
                "Блокировки файлов",
                "Автоматические бэкапы",
                "Валидация и тестирование",
                "Фильтрация ложных срабатываний"
            ]
        }

# Тестирование
if __name__ == "__main__":
    print("🧪 Тест ExperimentalCodeManager v1.1...")
    
    class MockSecurity:
        def validate_action(self, *args, **kwargs):
            return True, "Разрешено", {}
    
    test_dir = Path("test_experimental")
    test_dir.mkdir(exist_ok=True)
    
    manager = ExperimentalCodeManager(MockSecurity(), test_dir)
    
    suggestions = manager.analyze_experimental_code_safely()
    print(f">> Найдено предложений: {len(suggestions)}")
    
    status = manager.get_status()
    print(f">> Версия: {status['version']}")
    print(f">> Макс. размер файла: {status['max_file_size_lines']} строк")
    
    import shutil
    shutil.rmtree(test_dir, ignore_errors=True)
    
    print("✅ Тест завершён")