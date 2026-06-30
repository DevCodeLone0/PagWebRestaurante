#Prueba de Registrar Proveedor (Admin)
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

    #Login como admin
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys(ADMIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button.btn-auth").click()
    time.sleep(2)

    #Ir a proveedores
    driver.get(f"{BASE_URL}/proveedores")
    time.sleep(2)

    #Llenar formulario
    driver.find_element(By.ID, "nombre").send_keys("Proveedor Auto")
    driver.find_element(By.ID, "empresa").send_keys("Empresa Auto S.A.")
    driver.find_element(By.ID, "telefono").send_keys("555-0000")
    driver.find_element(By.ID, "email").send_keys("auto@proveedor.com")
    driver.find_element(By.ID, "producto").send_keys("Verduras")
    time.sleep(1)

    #Enviar
    driver.find_element(By.CSS_SELECTOR, "button.btn-submit").click()
    time.sleep(2)

    #Verificar
    errores = driver.find_elements(By.CSS_SELECTOR, ".flash.error")
    if len(errores) == 0:
        print("[PASS] Proveedor registrado exitosamente")
    else:
        print(f"[FAIL] Error al registrar proveedor: {errores[0].text}")

    driver.quit()

if __name__ == "__main__":
    main()
