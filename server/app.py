from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import random
import time
import uuid
from datetime import datetime
from flask_cors import CORS
from db import ConnectDB
from login import Login 

app = Flask(__name__)
CORS(app)
db = ConnectDB()
isLoggedIn = False
driver = None  # Initialize driver as None to manage persistent sessions

try:
    db.connect()
    print("Connected to MongoDB")
except Exception as e:
    print(e)

def account_info():
    with open('account_info.txt', 'r') as f:
        info = f.read().split()
        email = info[0]
        password = info[1]
    return email, password

def initialize_driver():
    """Initialize the Selenium driver if it hasn't been initialized yet."""
    global driver, isLoggedIn, proxy
    
    if driver is None:  # If the driver is not initialized, set it up
        print("Initializing WebDriver...")
        with open('proxy/valid_proxies.txt') as f:
            proxies = f.read().split('\n')
        proxy = random.choice(proxies)
        
        email, password = account_info()
        options = Options()
        # options.add_argument(f"--proxy-server=https://{proxy}") 
        # options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get("https://x.com/i/flow/login?redirect_after_login=%2Fexplore%3Fmx%3D2")

        with open('cookies.json', 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                cookie['domain'] = '.x.com'
                try:
                    driver.add_cookie(cookie)
                    isLoggedIn = True
                except Exception as e:
                    pass

        if not isLoggedIn:
            driver.get("https://x.com/i/flow/login")
            login = Login(email, password, driver)
            login.login(driver, email, password)
        else:
            driver.get("https://x.com/explore")
        print("WebDriver initialized and logged in.")

def fetch_trending_topics():
    """Fetch trending topics using the initialized WebDriver."""
    global driver, proxy

    # Navigate to Explore and scroll
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='AppTabBar_Explore_Link']"))
    )
    link.click()

    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 500);")

    time.sleep(2)

    trending_topics = []
    elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='trend']")

    for element in elements:
        parent_div = element.find_elements(By.TAG_NAME, "div")[0]
        child = parent_div.find_elements(By.TAG_NAME, "div")[2]
        trending_topics.append(child.text)

    print("Trending topics:", trending_topics)

    # Save the data to MongoDB
    timestamp = datetime.now()
    data = {
        "trends": trending_topics,
        "timestamp": timestamp,
        "ip_address": proxy
    }

    db.insert(data)
    print("Data saved successfully:", data)

    # Convert _id to string for JSON serialization
    data["_id"] = str(data["_id"])
    return data

@app.route('/trending', methods=['GET'])
def get_trending_topics():
    data = fetch_trending_topics()
    return jsonify({"status": "success", "data": data}), 200

@app.route('/end-session', methods=['GET'])
def end_session():
    global driver
    if driver is not None:
        driver.quit()
        driver = None
        print("WebDriver session ended.")
    return jsonify({"status": "success", "message": "Session ended"}), 200

@app.route('/')
def index():
    initialize_driver() 
    return "API is running"

if __name__ == '__main__':
    app.run(debug=True)
