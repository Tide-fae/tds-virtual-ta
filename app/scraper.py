from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

def extract_section_content(driver, url):
    """Extract text content from a section page"""
    try:
        print(f"📖 Extracting content from: {url}")
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = []
        for element in soup.select('.markdown-section p, .markdown-section h2, .markdown-section h3'):
            text = element.get_text(strip=True)
            if text:
                content.append(text)
        return content
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
        return []

def scrape_course_content():
    base_url = "https://tds.s-anand.net/#/2025-01/"
    course_data = []

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    driver.get(base_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    nav_items = soup.select('.sidebar-nav li a[href^="#/"]')

    for item in nav_items:
        section_name = item.get_text(strip=True)
        if not section_name:
            continue
        section_url = base_url + item['href'].lstrip('#')
        content = extract_section_content(driver, section_url)
        course_data.append({
            "section": section_name,
            "url": section_url,
            "content": content
        })
    with open("course_content.json", "w", encoding="utf-8") as f:
        json.dump(course_data, f, indent=2)
    driver.quit()
    return course_data

def scrape_discourse_posts():
    base_url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(base_url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    post_links = [a['href'] for a in soup.select('a.title') if a['href'].startswith('/t/')]
    
    discourse_data = []
    for link in post_links[:10]:  # limit to first 10 for demo
        full_url = "https://discourse.onlinedegree.iitm.ac.in" + link
        driver.get(full_url)
        time.sleep(3)
        post_soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = [p.get_text(strip=True) for p in post_soup.select('.post')]  # grabs post content
        discourse_data.append({
            "url": full_url,
            "content": content
        })
    with open("discourse_content.json", "w", encoding="utf-8") as f:
        json.dump(discourse_data, f, indent=2)
    driver.quit()
    return discourse_data

if __name__ == "__main__":
    scrape_course_content()
    scrape_discourse_posts()
