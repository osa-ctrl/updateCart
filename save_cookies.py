from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import json

def save_cookies(email, password, cookies_file="cookies.json"):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    try:
        driver.get("https://www.bestsecret.com/entrance/index.htm")
        time.sleep(2)

        try:
            accept_btn = driver.find_element(By.ID, "cmp-accept-all")
            accept_btn.click()
            time.sleep(1)
        except Exception:
            pass

        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)
        driver.find_element(By.NAME, "username").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(5)  # Ждем входа

        cookies = driver.get_cookies()
        with open(cookies_file, "w") as f:
            json.dump(cookies, f)
        print("✅ Cookies сохранены!")
    finally:
        driver.quit()