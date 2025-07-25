import inspect
from importlib import import_module

def load_module_source(module: str, tag: str):
    module_path = f"modules.{module}.source.source_{tag}"
    return import_module(module_path)

def load_module_logic(module: str, tag: str):
    module_path = f"modules.{module}.logic.logic_{tag}"
    return import_module(module_path)

def load_module_research():
    module_path = f"app.research.research"
    return import_module(module_path)

def check_source_items(source_module, column_map):
    functions = inspect.getmembers(source_module, inspect.isfunction)
    all_function = [name for name, _ in functions]
    for key in column_map.keys():
        if key not in all_function:
            return key
    return True

def extract_number(s: str) -> int:
    import re
    numeric_str = re.sub(r"[^\d]", "", s)
    return int(numeric_str) if numeric_str else 0  # 数字がなければ0を返す

def format_text(text: str) -> str:
    format_text = text.replace('\n', '').replace('\r', '').replace('\t', '').replace('\f', '').replace('\v', '')
    return format_text.strip()

if __name__ == "__main__":
    module = load_module_source("GREEN", "list")
    print(check_source_items(module))

"""
python -m app.utillities.utillities
"""