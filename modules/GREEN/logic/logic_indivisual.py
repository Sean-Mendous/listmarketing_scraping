import time
import json
from playwright.sync_api import sync_playwright
from app.utillities.utillities import load_module_source, load_module_research
from app.logger.logger import logger

indivisual_source_module = load_module_source("GREEN", "indivisual")

def run_flow(origin_column_map, spreadsheet, indivisual_source_module):
    message = f"""
\n--------------------------
WELCOME TO SOURCE: GREEN - indivisual
we are going to run flow.
here are some information, have a good day!:

scraping / o
research / o

web_type = Single Page Application
login = non-needed (headless = True)
--------------------------\n
"""
    logger.info(message)

    column_map =  {}
    if "list" in origin_column_map:
        column_map = column_map | origin_column_map["list"]
    if "indivisual" in origin_column_map:
        column_map = column_map | origin_column_map["indivisual"]
    if "research" in origin_column_map:
        column_map = column_map | origin_column_map["research"]
    if "system" in origin_column_map:
        column_map = column_map | origin_column_map["system"]
    
    from app.spreadsheet.spreadsheet import write_by_column, search_into_column

    try:
        unprocess_rows = search_into_column(spreadsheet["worksheet"], column_map["status"], "list_completed")
        if not unprocess_rows:
            logger.info("No unprocessed rows found.")
            return True
        logger.info(f"Found {len(unprocess_rows)} unprocessed rows.")
    except Exception as e:
        raise RuntimeError(f"Failed to search unprocessed rows: {e}")
    
    for unprocess_row in unprocess_rows:
        logger.info(f"Processing row: {unprocess_row + 1}")

        if "indivisual" in origin_column_map:
            try:
                indivisual_url = spreadsheet["worksheet"][column_map["recruitmenturl"]][unprocess_row].value
                if not indivisual_url:
                    logger.warning(f"No url found in row {unprocess_row + 1}")
                    continue
            except Exception as e:
                raise RuntimeError(f"Failed to get url: {e}")
            try:
                indivisual_url = fix_url(indivisual_url)
            except Exception as e:
                raise RuntimeError(f"Failed to fix url: {e}")
            try:
                scrape_result_map = playwright_flow(indivisual_url, origin_column_map["indivisual"], indivisual_source_module)
                if not scrape_result_map:
                    raise RuntimeError("Failed to get result")
                logger.info(f'scraping result:\n{json.dumps(scrape_result_map, indent=4, ensure_ascii=False)}')
            except Exception as e:
                raise RuntimeError(f"Failed to get result: {e}")
        else:
            scrape_result_map = None

        if "research" in origin_column_map:
            from app.research.research import define_case, find_variables, research_flow
            try:
                case = define_case(origin_column_map["research"])
            except Exception as e:
                raise RuntimeError(f"Failed to define case: {e}")
            try:
                company, website = find_variables(case, origin_column_map, scrape_result_map, spreadsheet, column_map, unprocess_row)
            except Exception as e:
                raise RuntimeError(f"Failed to find variables: {e}")
            try:
                research_result_map = research_flow(company, website)
            except Exception as e:
                raise RuntimeError(f"Failed to run research: {e}")
        
        result_map = {}
        if scrape_result_map:
            result_map = result_map | scrape_result_map
        if research_result_map:
            result_map = result_map | research_result_map

        try:
            result_map["status"] = "indivisual_completed"
            status = write_by_column(
                spreadsheet["original_path"],
                spreadsheet["workbook"],
                spreadsheet["worksheet"],
                unprocess_row + 1, # 読み取りが0始まりのため
                column_map,
                result_map
            )
            if not status:
                raise RuntimeError("Failed to write in spreadsheet")
            logger.info(f'written in spreadsheet ({unprocess_row})')
        except Exception as e:
            raise RuntimeError(f"Failed to write in spreadsheet: {e}")
        
        time.sleep(2)

    logger.info("All rows processed.")
    return True

def playwright_flow(url, key_column_map, indivisual_source_module):
    with sync_playwright() as p:
        try:
            from app.scraping.playwrite import open_url
            browser, page, context = open_url(url, p=p, headless=True)
            html = page.content()
        except Exception as e:
            raise RuntimeError(f"Failed to open url: {e}")

        result = {}
        for key in key_column_map.keys():
            try:
                value = getattr(indivisual_source_module, key)(html)
                result[key] = value if value else "None"
            except Exception as e:
                raise RuntimeError(f"Failed to run {key} function: {e}")
        page.close()
    return result

def fix_url(url):
    import re
    pattern = r"https://www\.green-japan\.com/company/(\d+)"
    match = re.search(pattern, url)
    if match:
        return f"https://www.green-japan.com/company/{match.group(1)}"
    else:
        return url

if __name__ == "__main__":
    # key_column_map = {
    #     "website": "A",
    #     "inquiry": "B",
    # }
    # responce = research_flow("株式会社 エージェントグロー", key_column_map, research_module)
    # print(responce)

    key_column_map = {
        "capitalstock": "A",
        "averageage": "B",
        "address": "C",
    }
    responce = playwright_flow("https://www.green-japan.com/company/4335", key_column_map, indivisual_source_module)
    print(responce)

"""
python -m modules.GREEN.logic.logic_indivisual
"""


        



    
