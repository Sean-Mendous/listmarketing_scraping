from bs4 import BeautifulSoup

def capitalstock(html):
    try:
        items = content(html)
    except Exception as e:
        return None
    
    try:
        for item in items:
            label = item.find('div', class_='MuiTypography-subtitle2')
            if label and label.get_text(strip=True) == '資本金':
                value = item.find('p', class_='MuiTypography-body2')
                return value.get_text(strip=True) if value else None
    except Exception as e:
        return None

    return None

def averageage(html):
    try:
        items = content(html)
    except Exception as e:
        return None
    
    try:
        for item in items:
            label = item.find('div', class_='MuiTypography-subtitle2')
            if label and label.get_text(strip=True) == '平均年齢':
                value = item.find('p', class_='MuiTypography-body2')
                return value.get_text(strip=True) if value else None
    except Exception as e:
        return None

    return None

def address(html):
    try:
        items = content(html)
    except Exception as e:
        return None
    
    try:
        for item in items:
            label = item.find('div', class_='MuiTypography-subtitle2')
            if label and label.get_text(strip=True) == '本社住所':
                value = item.find('p', class_='MuiTypography-body2')
                return value.get_text(strip=True) if value else None
    except Exception as e:
        return None

    return None

def content(html): # content
    soup = BeautifulSoup(html, 'html.parser')

    company_info_header = soup.find('h2', string='企業情報')
    if not company_info_header:
        return None
    
    container = company_info_header.find_parent('div')
    if not container:
        return None
    
    info_section = container.find('div', class_='css-ikzlcq')
    if not info_section:
        return None
    
    items = info_section.find_all('div', class_='css-1yjo05o')
    if not items:
        return None
    
    return items
