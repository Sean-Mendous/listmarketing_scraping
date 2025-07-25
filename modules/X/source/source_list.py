from bs4 import BeautifulSoup
from app.utillities.utillities import extract_number
from app.scraping.playwrite import scroll_page_human_like
from app.logger.logger import logger

def recruitmenturl(content):
    try:
        url_tag = content.find('a')
        if url_tag:
            url = url_tag['href']
            return url if url else None
        else:
            return None
    except (IndexError, AttributeError):
        return None

def name(content):
    try:
        name_section = content.find('span', attrs={'dir': 'ltr'})
        name_spans = name_section.find_all('span')
        if name_spans:
            name = name_spans[0]
            return name.text if name else None
        else:
            return None
    except (IndexError, AttributeError):
        return None
    
def role(content):
    try:
        text_section = content.find('div', class_='mb1')
        div_sections = text_section.find_all('div')
        if div_sections:
            role = div_sections[-2]
            return role.text if role else None
        else:
            return None
    except (IndexError, AttributeError):
        return None

def location(content):
    try:
        text_section = content.find('div', class_='mb1')
        div_sections = text_section.find_all('div')
        if div_sections:
            location = div_sections[-1]
            return location.text if location else None
        else:
            return None
    except (IndexError, AttributeError):
        return None
    
def content(page): # html
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    main_section = soup.find('main')
    if not main_section:
        raise RuntimeError('main_section is None')

    contents = main_section.find_all('li')
    if not contents:
        raise RuntimeError('contents is None')

    return contents

def click_next_button(page): #action
    try:
        scroll_page_human_like(page, max_attempts=2, same_height_threshold=5)
    except Exception as e:
        raise RuntimeError(f"Failed to scroll page: {e}")
    
    try:
        # 「aria-label="次へ"」のボタンを取得（最も信頼性が高い）
        next_button = page.get_by_role("button", name="次へ")

        # 表示されるまで最大5秒待機（非表示ならTimeout）
        next_button.wait_for(state="visible", timeout=5000)

        # ボタンが無効化されていたらスキップ
        if next_button.is_disabled():
            logger.info("Next button is disabled.")
            return False

        # ボタンをクリック
        next_button.click()
        return True

    except Exception as e:
        logger.error(f"Failed to click next button: {e}")
        return False