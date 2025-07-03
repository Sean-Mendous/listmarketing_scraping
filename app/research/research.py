from app.research.google_search_api import google_search_api, google_search_api_with_keyword
from app.logger.logger import logger

def research(company):
    logger.info(f'start researching: {company}')
    try:
        # # サイト検索
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

        # サイト検索
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

        # フォーム検索
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

    except Exception as e:
        logger.error(f'research error: {e}')
        return None, None

def find_company(origin_column_map):
    for phase_key in origin_column_map.keys():
        for column_key in origin_column_map[phase_key].keys():
            if column_key == "company":
                return phase_key
    return None
