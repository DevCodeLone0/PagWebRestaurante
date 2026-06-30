#Prueba de Registrar Plato (Admin)
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

    #Ir a platos
    driver.get(f"{BASE_URL}/platos")
    time.sleep(2)

    #Llenar formulario
    driver.find_element(By.ID, "nombre").send_keys("Plato Automatizado")
    driver.find_element(By.ID, "descripcion").send_keys("Plato creado por Selenium")
    driver.find_element(By.ID, "precio").send_keys("30.00")

    #Seleccionar categoria
    from selenium.webdriver.support.ui import Select
    select = Select(driver.find_element(By.ID, "categoria"))
    select.select_by_value("platos_fuertes")
    time.sleep(1)

    #Enviar
    driver.execute_script("document.querySelector('form').submit()")
    time.sleep(2)

    #Verificar que no hay error
    errores = driver.find_elements(By.CSS_SELECTOR, ".flash.error")
    if len(errores) == 0:
        print("[PASS] Plato registrado exitosamente")
    else:
        print(f"[FAIL] Error al registrar plato: {errores[0].text}")

    driver.quit()

if __name__ == "__main__":
    main()


