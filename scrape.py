from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
import time
from bs4 import BeautifulSoup

AUTH = 'brd-customer-hl_8f9925ea-zone-ai_scraper:opeieg1e8r7o'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(website):
    if not website.startswith("http"):
        website = "https://" + website

    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    options = ChromeOptions()
    options.add_argument("--headless=new")  # Faster

    with Remote(sbr_connection, options=options) as driver:
        driver.get(website)
        time.sleep(2)
        html = driver.execute_script("return document.body.outerHTML;")  # Faster than full page_source
    return html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return str(soup.body) if soup.body else ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    text = soup.get_text(separator="\n", strip=True)
    return "\n".join(line for line in text.splitlines() if line.strip())

def split_dom_content(dom_content, max_length=1500):
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]






  
