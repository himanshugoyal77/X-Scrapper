from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Login:
    def __init__(self, username, password, driver):
        self.driver = driver
        self.username = username
        self.password = password
        
    def login(self, driver, email, password):

        time.sleep(2)

        # login
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[name="text"]')
        email_input.send_keys(email)

        button = driver.find_element(By.XPATH, '//span[text()="Next"]')
        button.click()

        time.sleep(2)

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_input.send_keys(password)
        # hiteshgoyal943@gmail.com
        # find element by inner text
        button = driver.find_element(By.XPATH, '//span[text()="Log in"]')
        button.click()
        time.sleep(2)