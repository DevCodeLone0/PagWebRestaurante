#Funciones reutilizables para pruebas Selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def setup_browser():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1920, 1080")
    driver = Chrome(service=service, options=option)
    return driver

def login(driver, base_url, email, password):
    driver.get(f"{base_url}/login")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button.btn-auth").click()
    time.sleep(2)

def wait_and_find(driver, by, value):
    time.sleep(1)
    return driver.find_element(by, value)

def fill_field(driver, by, value, text):
    field = driver.find_element(by, value)
    field.clear()
    field.send_keys(text)

def select_option(driver, select_id, option_value):
    from selenium.webdriver.support.ui import Select
    select = Select(driver.find_element(By.ID, select_id))
    select.select_by_value(option_value)

def click_element(driver, by, value):
    driver.find_element(by, value).click()

def print_result(test_name, success, message=""):
    status = "PASS" if success else "FAIL"
    print(f"[{status}] {test_name}")
    if message:
        print(f"  -> {message}")
