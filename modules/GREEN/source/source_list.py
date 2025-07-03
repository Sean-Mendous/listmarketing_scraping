from bs4 import BeautifulSoup
from app.utillities.utillities import extract_number

def recruitmenturl(content):
    try:
        url = content.find('a')['href']
        return f'https://www.green-japan.com/{url}' if url else None
    except (IndexError, AttributeError):
        return None

def company(content):
    try:
        text_section = content.find('div', class_='css-tl5l2m')
        company = text_section.find('div')
        return company.text if company else None
    except (IndexError, AttributeError):
        return None

def people(content):
    try:
        text_section = content.find('div', class_='css-tl5l2m')
        people = text_section.find_all('div', class_='css-vb6e92')[0].find('p')
        return extract_number(people.text) if people else None
    except (IndexError, AttributeError):
        return None
    
def establishyear(content):
    try:
        text_section = content.find('div', class_='css-tl5l2m')
        establishyear = text_section.find_all('div', class_='css-vb6e92')[1].find('p')
        return extract_number(establishyear.text) if establishyear else None
    except (IndexError, AttributeError):
        return None
    
def content(page): # html
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')
    contents = soup.find_all('div', class_='MuiBox-root css-vfzywm')
    return contents

def click_next_button(page): # action
    try:
        next_button = page.locator('a:has(svg[data-testid="NavigateNextIcon"])').first
        if next_button.is_disabled() or not next_button.is_visible():
            return False  # 次へが無効 or 不可視なら終了
        next_button.click()
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to click next button: {e}")