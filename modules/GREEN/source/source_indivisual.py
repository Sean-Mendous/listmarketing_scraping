from bs4 import BeautifulSoup

def company(html):
    soup = BeautifulSoup(html, 'html.parser')
    main_section = soup.find('div', class_='css-ikzlcq')
    div_contents = main_section.find_all('div')
    for div in div_contents:
        text_div = div.find('div')
        lable_text = text_div.find('div').text
        if lable_text == '会社名':
            company = text_div.find('p').text
            return company

def address(html):
    pass
