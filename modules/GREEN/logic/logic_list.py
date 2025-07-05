import time
import json
from playwright.sync_api import sync_playwright
from app.utillities.utillities import load_module_source
from app.logger.logger import logger

list_source_module = load_module_source("GREEN", "list")
origin_url = "https://www.green-japan.com/search"

def run_flow(origin_column_map, spreadsheet, list_source_module):
    message = f"""
\n--------------------------
WELCOME TO SOURCE: GREEN - list
we are going to run flow.
here are some information, have a good day!:

web_type = Single Page Application
headless = False
    - search_type: manual
    - search_amount: one time only
--------------------------\n
"""
    logger.info(message)

    column_map = origin_column_map["list"] | origin_column_map["system"]

    try:
        for result_map, searchword in playwright_flow(origin_column_map["list"], list_source_module):
            if not result_map:
                logger.info("No contents found. Finishing flow.")
                return True

            logger.info(f'scraping result:\n{json.dumps(result_map, indent=4, ensure_ascii=False)}')

            try:
                from app.spreadsheet.spreadsheet import write_by_column
                result_map["status"] = "list_completed"
                result_map["searchword"] = searchword
                status = write_by_column(
                    spreadsheet["original_path"],
                    spreadsheet["workbook"],
                    spreadsheet["worksheet"],
                    spreadsheet["row"],
                    column_map,
                    result_map
                )
                if not status:
                    raise RuntimeError("Failed to write in spreadsheet")
                
                logger.info(f'written in spreadsheet ({spreadsheet["row"]})')
                spreadsheet["row"] += 1

            except Exception as e:
                raise RuntimeError(f"Failed to write in spreadsheet: {e}")
            
    except Exception as e:
        raise RuntimeError(f"Failed to run playwright flow: {e}")
    
    logger.info("No contents found. Finishing flow.")

def playwright_flow(key_column_map, list_source_module):
    with sync_playwright() as p:
        try:
            from app.scraping.playwrite import open_url
            browser, page, context = open_url(origin_url, p=p, headless=False)
        except Exception as e:
            raise RuntimeError(f"Failed to open url: {e}")

        try:
            searchword = input("検索条件を入力してください..: ")
        except Exception as e:
            raise RuntimeError(f"Failed to input search: {e}")

        for page_index in range(2, 1000):
            try:
                contents = getattr(list_source_module, "content")(page)
            except Exception:
                raise RuntimeError("Failed to get content")
            
            if not contents:
                yield None, None

            for i, c in enumerate(contents, start=1):
                result = {}
                for key in key_column_map.keys():
                    try:
                        value = getattr(list_source_module, key)(c)
                        result[key] = value if value else "None"
                    except Exception as e:
                        raise RuntimeError(f"Failed to run {key} function: {e}")
                
                yield result, searchword  # 個々の抽出結果をその都度返す

            try:
                status = getattr(list_source_module, "click_next_button")(page)
                if not status:
                    yield None, None
                logger.info("Success to run next action")
            except Exception as e:
                raise RuntimeError(f"Failed to run next action: {e}")

            time.sleep(1.5)

        page.close()


if __name__ == "__main__":
    key_column_map = {
        "company": "A",
        "people": "B",
        "establishyear": "C",
        "recruitmenturl": "D",
    }
    
    for responce in playwright_flow(key_column_map, list_source_module=list_source_module):
        print(responce)

"""
python -m modules.GREEN.logic.logic_list
"""


        



    
