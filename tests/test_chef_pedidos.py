#Prueba de Chef - Iniciar preparacion y marcar completo
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tests.config import BASE_URL, CHEF_EMAIL, CHEF_PASSWORD
import time

def main():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1920, 1080")
    driver = Chrome(service=service, options=option)

    #Login como chef
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys(CHEF_EMAIL)
    driver.find_element(By.ID, "password").send_keys(CHEF_PASSWORD)
    driver.execute_script("document.querySelector('form').submit()")
    time.sleep(2)

    #Ir a pedidos del chef
    driver.get(f"{BASE_URL}/chef/pedidos")
    time.sleep(2)

    #Verificar pedidos pendientes
    filas = driver.find_elements(By.CSS_SELECTOR, "table.orders-table tbody tr")
    print(f"  -> Pedidos encontrados: {len(filas)}")

    #Buscar boton de iniciar preparacion
    botones_start = driver.find_elements(By.CSS_SELECTOR, "a.btn-start")
    if len(botones_start) > 0:
        botones_start[0].click()
        time.sleep(2)
        print("[PASS] Inicio de preparacion exitoso")
    else:
        print("[SKIP] No hay pedidos pendientes para iniciar")

    #Buscar boton de completar
    botones_complete = driver.find_elements(By.CSS_SELECTOR, "a.btn-complete")
    if len(botones_complete) > 0:
        botones_complete[0].click()
        time.sleep(2)
        print("[PASS] Pedido completado exitosamente")
    else:
        print("[SKIP] No hay pedidos en preparacion para completar")

    driver.quit()

if __name__ == "__main__":
    main()


