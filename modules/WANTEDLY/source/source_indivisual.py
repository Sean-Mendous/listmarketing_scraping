from bs4 import BeautifulSoup

def profile(html):
    try:
        section = sections(html, None)
    except Exception as e:
        return None
    try:
        profile = section.find('div', class_='text-body-medium break-words')
        return profile.text if profile else None
    except Exception as e:
        return None

def biography(html):
    try:
        section = sections(html, "自己紹介")
    except Exception as e:
        return None
    try:
        div_section = section.find('div', class_='display-flex ph5 pv3')
        if not div_section:
            return None
        span_section = div_section.find('span')
        if not span_section:
            return None
        return span_section.text if span_section else None
    except Exception as e:
        return None
    
def recentactivity(html):
    try:
        section = sections(html, "アクティビティ")
    except Exception as e:
        return None
    try:
        ul_tag = section.find('ul')
        if not ul_tag:
            return None
        li_tag = ul_tag.find('li')
        if not li_tag:
            return None
        
        div_tag = li_tag.find('div', class_='update-components-actor__meta')
        if not div_tag:
            return None

        sub_desc = div_tag.find("span", class_="update-components-actor__sub-description")
        if not sub_desc:
            return None

        inner_span = sub_desc.find("span", attrs={"aria-hidden": "true"})
        if not inner_span:
            return None

        return inner_span.text if inner_span else None
    except Exception as e:
        return None
    
def career(html):
    try:
        section = sections(html, "職歴")
    except Exception as e:
        return None
    try:
        ul_tag = section.find('ul')
        if not ul_tag:
            return None
        
        li_tag = ul_tag.find('li')
        if not li_tag:
            return None

        return li_tag.text if li_tag else None
    except Exception as e:
        return None

def sections(html, keyword): # content
    soup = BeautifulSoup(html, 'html.parser')

    main_section = soup.find('main')
    if not main_section:
        raise RuntimeError("main_section is None")
    
    sections = main_section.find_all("section", recursive=False)
    if not sections:
        raise RuntimeError("sections are None")
    
    if not keyword:
        return sections[0]
    
    for section in sections:
        h2_tag = section.find("h2")
        if not h2_tag:
            continue
        if keyword in h2_tag.text:
            return section
    return None
