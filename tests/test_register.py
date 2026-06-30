#Prueba de Registro de Cliente
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tests.config import BASE_URL
import time

def main():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1920, 1080")
    driver = Chrome(service=service, options=option)

    driver.get(f"{BASE_URL}/register")
    time.sleep(2)

    driver.find_element(By.ID, "nombre").send_keys("Juan Test")
    driver.find_element(By.ID, "telefono").send_keys("555-9999")
    driver.find_element(By.ID, "direccion").send_keys("Calle Test 456")
    driver.find_element(By.ID, "email").send_keys("juan@test.com")
    driver.find_element(By.ID, "password").send_keys("Juan1234")
    driver.find_element(By.ID, "confirm_password").send_keys("Juan1234")
    driver.find_element(By.CSS_SELECTOR, "button.btn-auth").click()
    time.sleep(2)

    if "/login" in driver.current_url:
        print("[PASS] Registro exitoso, redirige a /login")
    else:
        print("[FAIL] Registro fallido")

    driver.quit()

if __name__ == "__main__":
    main()
