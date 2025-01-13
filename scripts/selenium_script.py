from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pymongo
import uuid

# Step 1: Configure ProxyMesh
proxy_username = "your_proxymesh_username"
proxy_password = "your_proxymesh_password"
proxy_url = f"http://{proxy_username}:{proxy_password}@us.proxymesh.com:31280"

# Step 2: Configure Selenium WebDriver with proxy
options = Options()
options.add_argument(f"--proxy-server={proxy_url}")
service = Service('path/to/chromedriver')  # Replace with your ChromeDriver path
driver = webdriver.Chrome(service=service, options=options)

# Step 3: Log in to Twitter
def login_to_twitter():
    driver.get("https://twitter.com/login")
    username = driver.find_element(By.NAME, "text")
    username.send_keys("your_twitter_username")  # Replace with your username
    username.send_keys(Keys.RETURN)

    driver.implicitly_wait(3)
    password = driver.find_element(By.NAME, "password")
    password.send_keys("your_twitter_password")  # Replace with your password
    password.send_keys(Keys.RETURN)

# Step 4: Scrape Trending Topics
def scrape_trending_topics():
    driver.implicitly_wait(5)
    trends = driver.find_elements(By.CSS_SELECTOR, "section[aria-labelledby='accessible-list-1'] div span")
    trending_topics = [trend.text for trend in trends[:5]]
    return trending_topics

# Step 5: Store Results in MongoDB
def save_to_mongodb(trending_topics, ip_address):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["twitter_trends"]
    collection = db["trends"]

    record = {
        "_id": str(uuid.uuid4()),
        "trends": trending_topics,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": ip_address,
    }
    collection.insert_one(record)
    return record

# Step 6: Get Current IP Address (Verify ProxyMesh IP Rotation)
def get_ip_address():
    import requests
    response = requests.get("http://httpbin.org/ip", proxies={"http": proxy_url, "https": proxy_url})
    return response.json()["origin"]

# Run the Script
try:
    login_to_twitter()
    topics = scrape_trending_topics()
    ip = get_ip_address()
    saved_record = save_to_mongodb(topics, ip)
    print("Data saved to MongoDB:", saved_record)
finally:
    driver.quit()
 
