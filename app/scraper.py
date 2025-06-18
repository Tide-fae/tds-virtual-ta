import sys
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

def get_driver():
    """Initialize ChromeDriver manually without Selenium Manager"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ✅ Disable Selenium Manager forcing manual driver path
    os.environ['SELENIUM_MANAGER'] = '0'

    driver_path = r"C:\Users\91933\Documents\tds-virtual-ta\drivers\chromedriver.exe"  # Update this if driver path changes
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def extract_section_content(driver, url):
    """Extract text content from a section page"""
    try:
        print(f"📖 Extracting content from: {url}")
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return [
            element.get_text(strip=True)
            for element in soup.select('.markdown-section p, .markdown-section h2, .markdown-section h3')
            if element.get_text(strip=True)
        ]
    except Exception as e:
        print(f"⚠️ Error extracting {url}: {str(e)}")
        return []

def scrape_course_content():
    """Scrape course content from main website"""
    base_url = "https://tds.s-anand.net/#/2025-01/"
    course_data = []
    driver = None

    try:
        driver = get_driver()
        driver.get(base_url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for item in soup.select('.sidebar-nav li a[href^="#/"]'):
            if section_name := item.get_text(strip=True):
                section_url = base_url + item['href'].lstrip('#')
                course_data.append({
                    "section": section_name,
                    "url": section_url,
                    "content": extract_section_content(driver, section_url)
                })

        with open("course_content.json", "w", encoding="utf-8") as f:
            json.dump(course_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"🚨 Course scraping error: {str(e)}")
    finally:
        if driver:
            driver.quit()

    return course_data

def scrape_discourse_posts():
    """Scrape discussion posts from Discourse forum"""
    base_url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"
    discourse_data = []
    driver = None

    try:
        driver = get_driver()
        driver.get(base_url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for link in [a['href'] for a in soup.select('a.title') if a['href'].startswith('/t/')][:10]:
            full_url = "https://discourse.onlinedegree.iitm.ac.in" + link
            driver.get(full_url)
            time.sleep(3)
            discourse_data.append({
                "url": full_url,
                "content": [
                    p.get_text(strip=True)
                    for p in BeautifulSoup(driver.page_source, 'html.parser').select('.post')
                ]
            })

        with open("discourse_content.json", "w", encoding="utf-8") as f:
            json.dump(discourse_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"🚨 Discourse scraping error: {str(e)}")
    finally:
        if driver:
            driver.quit()

    return discourse_data

if __name__ == "__main__":
    print("🚀 Starting course content scrape...")
    if course_data := scrape_course_content():
        print(f"✅ Scraped {len(course_data)} sections")

    print("🚀 Starting discourse scrape...")
    if discourse_data := scrape_discourse_posts():
        print(f"✅ Scraped {len(discourse_data)} posts")
