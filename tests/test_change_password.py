#Prueba de Cambio de Contrasena
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
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
    driver.execute_script("document.querySelector('form').submit()")
    time.sleep(3)

    print(f"  -> After login URL: {driver.current_url}")

    #Si redirige a change_password, ya esta ahi
    if "/change_password" not in driver.current_url:
        driver.get(f"{BASE_URL}/change_password")
        time.sleep(2)

    driver.find_element(By.ID, "current_password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.ID, "new_password").send_keys("Admin5678")
    driver.find_element(By.ID, "confirm_password").send_keys("Admin5678")
    driver.execute_script("document.querySelector('form').submit()")
    time.sleep(3)

    print(f"  -> After change URL: {driver.current_url}")

    if "/restaurante" in driver.current_url or "/admin" in driver.current_url:
        print("[PASS] Cambio de contrasena exitoso")
    else:
        flashes = driver.find_elements(By.CSS_SELECTOR, ".flash")
        for f in flashes:
            print(f"  -> Flash: {f.text}")
        print("[FAIL] Cambio de contrasena fallido")

    #Restaurar contrasena original
    driver.get(f"{BASE_URL}/change_password")
    time.sleep(2)
    driver.find_element(By.ID, "current_password").send_keys("Admin5678")
    driver.find_element(By.ID, "new_password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.ID, "confirm_password").send_keys(ADMIN_PASSWORD)
    driver.execute_script("document.querySelector('form').submit()")
    time.sleep(2)

    driver.quit()

if __name__ == "__main__":
    main()