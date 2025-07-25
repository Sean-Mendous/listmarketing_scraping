import time
import json
from playwright.sync_api import sync_playwright
from app.utillities.utillities import load_module_source, format_text
from app.scraping.playwrite import open_url, scroll_page_human_like
from app.logger.logger import logger

indivisual_source_module = load_module_source("LINKEDIN", "indivisual")

def run_flow(origin_column_map, spreadsheet, indivisual_source_module):
    message = f"""
\n--------------------------
WELCOME TO SOURCE: LINKEDIN - indivisual
we are going to run flow.
here are some information, have a good day!:

scraping / o
research / x

web_type = Single Page Application
login = needed (headless = False)
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
    
    if "indivisual" in origin_column_map:
        with sync_playwright() as p:
            browser, page, context = open_url('https://www.linkedin.com/login', p=p, headless=False)
            input("Enter to continue...")

            for unprocess_row in unprocess_rows:
                logger.info(f"Processing row: {unprocess_row + 1}")

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
                    scrape_result_map = playwright_flow(indivisual_url, origin_column_map["indivisual"], indivisual_source_module, page)
                    if not scrape_result_map:
                        raise RuntimeError("Failed to get result")
                except Exception as e:
                    raise RuntimeError(f"Failed to get result: {e}")
                
                result_map = {}
                if scrape_result_map:
                    result_map = result_map | scrape_result_map

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
                    logger.info(f'scraping result:\n{json.dumps(scrape_result_map, indent=4, ensure_ascii=False)}')
                except Exception as e:
                    raise RuntimeError(f"Failed to write in spreadsheet: {e}")
                
                time.sleep(2)
    else:
        raise RuntimeError("Did not find any keys in origin_column_map")

    logger.info("All rows processed.")
    return True

def playwright_flow(url, key_column_map, indivisual_source_module, page):
    def get_result(url, page):
        try:
            page.goto(url, wait_until="load")
            scroll_page_human_like(page, max_attempts=1, same_height_threshold=5)
            html = page.content()
        except Exception as e:
            raise RuntimeError(f"Failed to get html: {e}")
        
        result = {}
        for key in key_column_map.keys():
            try:
                value = getattr(indivisual_source_module, key)(html)
                result[key] = format_text(value) if value else None
            except Exception as e:
                raise RuntimeError(f"Failed to run {key} function: {e}")
        return result

    if not page:
        with sync_playwright() as p:
            logger.info("No playwright instance provided. Opening login page.")
            browser, page, context = open_url('https://www.linkedin.com/login', p, headless=False)
            input("Enter to continue...")
            result = get_result(url, page)
            return result
    else:
        result = get_result(url, page)
        return result

def fix_url(url):
    import re
    pattern = r"https:\/\/www\.linkedin\.com\/in\/([^?\/]+)\?"
    match = re.search(pattern, url)
    if match:
        return f"https://www.linkedin.com/in/{match.group(1)}"
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
        "profile": "A",
        "biography": "B",
        "recentactivity": "C",
    }
    responce = playwright_flow("https://www.linkedin.com/in/andrew-youngil-lee/", key_column_map, indivisual_source_module, page=None)
    print(f"\n{json.dumps(responce, indent=4, ensure_ascii=False)}\n")

    # urls = [
    #     "https://www.linkedin.com/in/andrew-youngil-lee/",
    #     "https://www.linkedin.com/in/yun-tran-855191312",
    #     "https://www.linkedin.com/in/%E5%95%93%E5%A4%AA%E9%83%8E-%E5%AE%8D%E6%88%B8-8458a2a3",
    #     "https://www.linkedin.com/in/hisami-takesawa-5aa945143",
    # ]
    # test(urls)

"""
python -m modules.LINKEDIN.logic.logic_indivisual
"""


        



    
