import os
import openpyxl
from app.logger.logger import logger

from app.questionary.questionary import ask_client_folder
selected_client = ask_client_folder()

from app.questionary.questionary import ask_logic
selected_logic = ask_logic()

try:
    from app.yaml.parse import parse
    source, output_filename, output_sheetname, origin_column_map = parse(f"clients/{selected_client}/config.yaml")
except Exception as e:
    raise RuntimeError(f"Failed to parse yaml: {e}")

output_file_path = f"clients/{selected_client}/{output_filename}.xlsx"
if os.path.exists(output_file_path):
    logger.info(f"output file already exists: {output_filename}")
    file_exists = True
else:
    logger.info(f"output file does not exist: {output_filename}")
    file_exists = False

from app.utillities.utillities import load_module_source, load_module_logic, check_source_items
selected_source_module = load_module_source(source, selected_logic)
selected_logic_module = load_module_logic(source, selected_logic)
if selected_logic == "indivisual" and "indivisual" not in origin_column_map and "research" in origin_column_map: # indivisualなし / researchあり
    pass
else:
    if not check_source_items(selected_source_module, origin_column_map[selected_logic]) == True:
        raise RuntimeError(f"client config does not match source module: {check_source_items(selected_source_module, origin_column_map[selected_logic])}")

from app.spreadsheet.spreadsheet import create_workbook, acquisition_workbook, detect_row

if selected_logic == "list":
    try:
        if file_exists:
            workbook, worksheet = acquisition_workbook(output_file_path, output_sheetname)
            row = detect_row(output_file_path, output_sheetname)
            logger.info(f"using file: {output_filename}")
        else:
            workbook, worksheet = create_workbook(output_file_path, output_sheetname, origin_column_map)
            row = 2
            logger.info(f"created file: {output_filename}")
    except Exception as e:
        raise RuntimeError(f"Failed to check output file: {e}")
    
    spreadsheet = {
        "original_path": output_file_path,
        "workbook": workbook,
        "worksheet": worksheet,
        "row": row
    }
    
    try:
        status = getattr(selected_logic_module, "run_flow")(origin_column_map, spreadsheet, selected_source_module)
    except Exception as e:
        raise RuntimeError(f"Failed to run list: {e}")

if selected_logic == "indivisual":
    try:
        if file_exists:
            workbook, worksheet = acquisition_workbook(output_file_path, output_sheetname)
            logger.info(f"using file: {output_filename}")
        else:
            raise RuntimeError(f"output file does not exist: {output_filename}")
    except Exception as e:
        raise RuntimeError(f"Failed to check output file: {e}")

    spreadsheet = {
        "original_path": output_file_path,
        "workbook": workbook,
        "worksheet": worksheet,
        "row": None
    }
    
    try:
        status = getattr(selected_logic_module, "run_flow")(origin_column_map, spreadsheet, selected_source_module)
    except Exception as e:
        raise RuntimeError(f"Failed to run list: {e}")

if status:
    logger.info("🔥 Finished flow 🔥")






