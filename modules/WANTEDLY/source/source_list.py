import re
from bs4 import BeautifulSoup
from app.utillities.utillities import extract_number
from app.scraping.playwrite import scroll_page_human_like
from app.logger.logger import logger

def recruitmenturl(content):
    try:
        url_tags = content.find_all('a')
        if url_tags:
            url = url_tags[0]['href']
            return f'https://www.wantedly.com{url}' if url else None
        else:
            return None
    except (IndexError, AttributeError):
        return None
    
def companyurl(content):
    try:
        url_tags = content.find_all('a')
        if url_tags:
            url = url_tags[-1]['href']
            return f'https://www.wantedly.com{url}' if url else None
        else:
            return None
    except (IndexError, AttributeError):
        return None

def recruittitle(content):
    try:
        title_section = content.find('h2')
        if title_section:
            title = title_section.text
            return title if title else None
        else:
            return None
    except (IndexError, AttributeError):
        return None
    
def tags(content):
    try:
        tag_section = content.find('ul')
        if not tag_section:
            return None
        
        tags = tag_section.find_all('li')
        if tags:
            tag_list = []
            for tag in tags:
                tag_text = tag.text
                if tag_text:
                    tag_list.append(tag_text)
            tag_str = ', '.join(tag_list)
            return tag_str
        else:
            return None
    except (IndexError, AttributeError):
        return None

def details(content):
    try:
        text_section = content.find('p')
        if text_section:
            details = text_section.text
            return details if details else None
        else:
            return None
    except (IndexError, AttributeError):
        return None
    
def content(page): # html
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    main_section = soup.find('ul', class_=re.compile(r'\bProjectListJobPostsLaptop__ProjectList\b'))
    if not main_section:
        raise RuntimeError('main_section is None')

    contents = main_section.find_all('li')
    if not contents:
        raise RuntimeError('contents is None')

    return contents

def click_next_button(page):
    # try:
    #     scroll_page_human_like(page, max_attempts=2, same_height_threshold=5)
    # except Exception as e:
    #     raise RuntimeError(f"Failed to scroll page: {e}")

    try:
        # aria-labelを直接指定して取得
        next_button = page.locator('button[aria-label="Go to next page"]')

        # 表示されるまで待機（最大5秒）
        next_button.wait_for(state="visible", timeout=5000)

        # ボタンが無効化されていないか確認
        if next_button.is_disabled():
            raise RuntimeError("Next button is disabled.")

        # クリック実行
        next_button.click()
        return True

    except Exception as e:
        logger.error(f"Failed to click next button: {e}")
        return False