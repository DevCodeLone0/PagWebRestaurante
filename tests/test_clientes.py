#Prueba de Registrar Cliente (Mesero)
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tests.config import BASE_URL, MESERO_EMAIL, MESERO_PASSWORD
import time

def main():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1920, 1080")
    driver = Chrome(service=service, options=option)

    #Login como mesero
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys(MESERO_EMAIL)
    driver.find_element(By.ID, "password").send_keys(MESERO_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button.btn-auth").click()
    time.sleep(2)

    #Ir a clientes
    driver.get(f"{BASE_URL}/clientes")
    time.sleep(2)

    #Llenar formulario
    driver.find_element(By.ID, "nombre").send_keys("Cliente Selenium")
    driver.find_element(By.ID, "telefono").send_keys("555-1111")
    driver.find_element(By.ID, "direccion").send_keys("Av. Selenium 789")
    time.sleep(1)

    #Enviar
    driver.find_element(By.CSS_SELECTOR, "button.btn-submit").click()
    time.sleep(2)

    #Verificar
    errores = driver.find_elements(By.CSS_SELECTOR, ".flash.error")
    if len(errores) == 0:
        print("[PASS] Cliente registrado exitosamente")
    else:
        print(f"[FAIL] Error al registrar cliente: {errores[0].text}")

    driver.quit()

if __name__ == "__main__":
    main()
