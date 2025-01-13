from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import hashlib

driver = None
displayed_posts = set()

def initialize_driver():
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-data-dir=C:/Users/timlu/AppData/Local/Google/Chrome/User Data/")
        chrome_options.add_argument("profile-directory=Profile 11")
        service = Service("C:/tools/chromedriver/chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.linkedin.com/feed/")
        time.sleep(3)  # Kürzer initialisieren
    return driver

def remove_full_height():
    global driver
    driver.execute_script("""
        document.querySelectorAll('.full-height').forEach(element => {
            element.style.height = 'auto';
        });
    """)
    print("Removed inline height from .full-height")

def scroll_page():
    global driver
    if driver is None:
        raise Exception("Driver ist nicht initialisiert.")
    driver.execute_script("window.scrollBy(0, 600);")  # Größere Sprünge scrollen
    time.sleep(0.5)

def scrape_posts():
    global driver, displayed_posts
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    posts = []

    for post in soup.select(".feed-shared-update-v2"):
        try:
            text_element = post.select_one(".feed-shared-update-v2__description")
            text = text_element.get_text("\n", strip=True) if text_element else "Kein Text gefunden"

            profile_image_element = post.select_one(".ivm-view-attr__img--centered")
            profile_image_src = profile_image_element['src'] if profile_image_element else "Kein Profilbild gefunden"

            image_element = post.select_one(".update-components-image--single-image img")
            image_src = image_element['src'] if image_element else "Kein Bild gefunden"

            post_hash = hashlib.sha256((text + profile_image_src).encode()).hexdigest()
            if post_hash not in displayed_posts:
                displayed_posts.add(post_hash)
                posts.append({
                    "text": text,
                    "profile_image": profile_image_src,
                    "image": image_src
                })
        except Exception as e:
            print(f"Fehler beim Scrapen eines Beitrags: {e}")
    return posts

def reload_feed():
    global driver
    if driver is None:
        raise Exception("Driver ist nicht initialisiert.")
    driver.refresh()
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    remove_full_height()

def manage_buffer(threshold=5):  # Mehr Beiträge auf einmal
    global driver
    if driver is None:
        raise Exception("Driver ist nicht initialisiert.")
    buffer = []
    while len(buffer) < threshold:
        scroll_page()
        new_posts = scrape_posts()
        if not new_posts:
            break
        buffer.extend(new_posts)
    return buffer

def cleanup_driver():
    global driver
    if driver is not None:
        driver.quit()
        driver = None
