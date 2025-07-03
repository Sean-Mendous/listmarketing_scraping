import time
import json
import random
from app.logger.logger import logger

def open_url(url, p, headless=True):
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url, wait_until="load") 
    return browser, page, context

def login(context, page, cookie_path='app/scraping_setting/cookies.json'):
    with open(cookie_path, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    context.add_cookies(cookies)
    logger.info(f"used cookies / reload page")
    page.reload()

def logout(context, cookie_path='app/scraping_setting/cookies.json'):
    cookies = context.cookies()
    with open(cookie_path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2, ensure_ascii=False)
    logger.info(f"saved cookies")

def scroll_page_human_like(page, max_attempts=50, same_height_threshold=5):
    same_height_count = 0
    last_height = page.evaluate("document.body.scrollHeight")

    for attempt in range(max_attempts):
        step = random.randint(300, 1000)
        page.mouse.wheel(0, step)
        time.sleep(random.uniform(1, 3))

        new_height = page.evaluate("document.body.scrollHeight")

        if new_height == last_height:
            same_height_count += 1
        else:
            same_height_count = 0

        last_height = new_height

        if same_height_count >= same_height_threshold:
            break

        logger.info(f"scroll {attempt+1} times")
    
    html = page.content()
    return html
