#Prueba de Admin - Crear usuario y Toggle Active
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

    #Login como admin
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys(ADMIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(ADMIN_PASSWORD)
    driver.execute_script("document.querySelector('form').submit()")
    time.sleep(2)

    #Ir a users
    driver.get(f"{BASE_URL}/admin/users")
    time.sleep(2)

    #Crear usuario
    driver.get(f"{BASE_URL}/admin/users/create")
    time.sleep(2)

    driver.find_element(By.ID, "email").send_keys("nuevo@test.com")
    driver.find_element(By.ID, "password").send_keys("Nuevo1234")
    driver.find_element(By.ID, "confirm_password").send_keys("Nuevo1234")

    from selenium.webdriver.support.ui import Select
    select = Select(driver.find_element(By.ID, "rol"))
    select.select_by_value("mesero")
    time.sleep(1)

    driver.execute_script("document.querySelector('form').submit()")
    time.sleep(2)

    #Verificar creacion
    driver.get(f"{BASE_URL}/admin/users")
    time.sleep(2)
    usuarios = driver.find_elements(By.XPATH, "//td[contains(text(),'nuevo@test.com')]")
    if len(usuarios) > 0:
        print("[PASS] Usuario creado exitosamente")
    else:
        print("[FAIL] Usuario no se creo")

    driver.quit()

if __name__ == "__main__":
    main()


