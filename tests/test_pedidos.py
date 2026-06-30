#Prueba de Ver Pedidos
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

    #Ir a pedidos
    driver.get(f"{BASE_URL}/pedidos")
    time.sleep(2)

    #Verificar tabla de pedidos
    tabla = driver.find_elements(By.CSS_SELECTOR, "table.orders-table")
    if len(tabla) > 0:
        print("[PASS] Tabla de pedidos visible")
    else:
        print("[FAIL] Tabla de pedidos no encontrada")

    #Verificar filas
    filas = driver.find_elements(By.CSS_SELECTOR, "table.orders-table tbody tr")
    print(f"  -> Pedidos encontrados: {len(filas)}")

    driver.quit()

if __name__ == "__main__":
    main()
