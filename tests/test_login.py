#Prueba de Login valido e invalido
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tests.config import BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD
import time

def main():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1920, 1080")
    driver = Chrome(service=service, options=option)

    #Login valido con admin
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys(ADMIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button.btn-auth").click()
    time.sleep(2)

    if "/restaurante" in driver.current_url:
        print("[PASS] Login valido con admin")
    else:
        print("[FAIL] Login valido con admin")

    #Logout
    driver.get(f"{BASE_URL}/logout")
    time.sleep(2)

    #Login invalido
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys("wrong@email.com")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button.btn-auth").click()
    time.sleep(2)

    if "/login" in driver.current_url:
        print("[PASS] Login invalido redirige a /login")
    else:
        print("[FAIL] Login invalido no redirige a /login")

    driver.quit()

if __name__ == "__main__":
    main()
