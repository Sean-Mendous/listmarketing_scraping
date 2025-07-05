from app.research.google_search_api import google_search_api, google_search_api_with_keyword
from app.logger.logger import logger

def research(company, website):
    if company and not website:
        # サイト検索
        logger.info(f'start researching: {company}')

        # try:
        #     searchword = f'{company} 企業サイト'
        #     website = google_search_api_with_keyword(searchword, company, max_results=10)
        # except Exception as e:
        #     logger.error(f'google search error: {e}')

        # if not website:
        #     website = None
        #     logger.info('website: not found')
        # else:
        #     logger.info(f'website: {website}')

        try:
            searchword = f'{company} 企業サイト'
            website = google_search_api(searchword, max_results=1)
            website = website[0]['link'] if website else None
        except Exception as e:
            logger.error(f'google search error: {e}')

        if not website:
            logger.info('website: not found')
            logger.info('inquiry: not found')
            return None, None
        else:
            logger.info(f'website: {website}')

    if website:
        # フォーム検索
        logger.info(f'start researching: {company}')

        try:
            searchword = f'site:{website} 問い合わせ'
            inquiry = google_search_api(searchword, max_results=1)
            inquiry = inquiry[0]['link'] if inquiry else None
        except Exception as e:
            logger.error(f'form search error: {e}')

        if not inquiry:
            inquiry = None
            logger.info('inquiry: not found')
        else:
            logger.info(f'inquiry: {inquiry}')

    return website, inquiry

def find_company(origin_column_map):
    for phase_key in origin_column_map.keys():
        for column_key in origin_column_map[phase_key].keys():
            if column_key == "company":
                return phase_key
    return None

def find_website(origin_column_map):
    for phase_key in origin_column_map.keys():
        for column_key in origin_column_map[phase_key].keys():
            if column_key == "website":
                return phase_key
    return None

def define_case(key_column_map):
    if "website" in key_column_map and "inquiry" in key_column_map:
        return 1
    elif "inquiry" in key_column_map:
        return 2
    else:
        raise RuntimeError(f"Please check the conbination of key in column_map. {key_column_map}")
    
def find_variables(case: int, origin_column_map: dict, scrape_result_map: dict, spreadsheet: dict, column_map: dict, unprocess_row: int):
    if case == 1: # website & inquiry
        try:
            phase = find_company(origin_column_map)
            if not phase:
                raise RuntimeError("Failed to find company in column_map. Please add company to column_map to get research result.")
            if phase == "list":
                company = spreadsheet["worksheet"][column_map["company"]][unprocess_row].value
            elif phase == "indivisual":
                company = scrape_result_map["company"]
        except Exception as e:
            raise RuntimeError(f"Failed to find company: {e}")
        if not company:
            raise RuntimeError("Failed to find company. Please add company to column_map to get research result.")
        website = None
    if case == 2: # inquiry
        try:
            phase = find_website(origin_column_map)
            if not phase:
                raise RuntimeError("Failed to find website in column_map. Please add website to column_map to get research result.")
            if phase == "list":
                website = spreadsheet["worksheet"][column_map["website"]][unprocess_row].value
            elif phase == "indivisual":
                website = scrape_result_map["website"]
        except Exception as e:
            raise RuntimeError(f"Failed to find website: {e}")
        if not website:
            raise RuntimeError("Failed to find website. Please add website to column_map to get research result.")
        company = None

    if case != 1 and case != 2:
        raise RuntimeError(f"Please check the case. {case}")
    
    return company, website

def research_flow(company, website):
    try:
        website, inquiry = research(company, website)
    except Exception as e:
        raise RuntimeError(f"Failed to run research: {e}")
    
    result = {}
    result["website"] = website
    result["inquiry"] = inquiry

    return result
