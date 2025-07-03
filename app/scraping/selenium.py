import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app.logger_setting.logger import logger

def open_url(url, window_whosh=True):
    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")  # ミュートオプション
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.set_window_size(1280, 800)

    if window_whosh:
        browser.set_window_position(-2000, 0)
    
    browser.get(url)
    return browser

def login(browser, cookie):
    with open(cookie, "r") as file:
        cookies = json.load(file)
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.refresh()
    return None

def logout(browser, cookie):
    cookies = browser.get_cookies()
    with open(cookie, "w") as file:
        json.dump(cookies, file)
    browser.quit()
    return None
    

if __name__ == "__main__":
    browser = open_url("https://www.tiktok.com/", window_whosh=False)
    input()
    logout(browser, 'cookies.json')
    browser.quit()

"""
python -m app.scraping.selenium_setting
"""
