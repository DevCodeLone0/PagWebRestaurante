#Prueba de Cambio de Contrasena
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

    #Login
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys(ADMIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button.btn-auth").click()
    time.sleep(2)

    #Ir a cambiar contrasena
    driver.get(f"{BASE_URL}/change_password")
    time.sleep(2)

    driver.find_element(By.ID, "current_password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.ID, "new_password").send_keys("Admin5678")
    driver.find_element(By.ID, "confirm_password").send_keys("Admin5678")
    driver.find_element(By.CSS_SELECTOR, "button.btn-auth").click()
    time.sleep(2)

    if "/restaurante" in driver.current_url:
        print("[PASS] Cambio de contrasena exitoso")
    else:
        print("[FAIL] Cambio de contrasena fallido")

    #Restaurar contrasena original
    driver.get(f"{BASE_URL}/change_password")
    time.sleep(2)
    driver.find_element(By.ID, "current_password").send_keys("Admin5678")
    driver.find_element(By.ID, "new_password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.ID, "confirm_password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button.btn-auth").click()
    time.sleep(2)

    driver.quit()

if __name__ == "__main__":
    main()
