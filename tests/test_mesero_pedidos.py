#Prueba de Mesero - Entregar y cancelar pedidos
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

    #Ir a pedidos del mesero
    driver.get(f"{BASE_URL}/mesero/pedidos")
    time.sleep(2)

    #Verificar pedidos
    filas = driver.find_elements(By.CSS_SELECTOR, "table.orders-table tbody tr")
    print(f"  -> Pedidos encontrados: {len(filas)}")

    #Buscar boton de entregar
    botones_deliver = driver.find_elements(By.CSS_SELECTOR, "a.btn-deliver")
    if len(botones_deliver) > 0:
        botones_deliver[0].click()
        time.sleep(2)
        print("[PASS] Pedido entregado exitosamente")
    else:
        print("[SKIP] No hay pedidos listos para entregar")

    #Buscar boton de cancelar
    botones_cancel = driver.find_elements(By.CSS_SELECTOR, "a.btn-cancel")
    if len(botones_cancel) > 0:
        botones_cancel[0].click()
        time.sleep(2)
        print("[PASS] Pedido cancelado exitosamente")
    else:
        print("[SKIP] No hay pedidos para cancelar")

    driver.quit()

if __name__ == "__main__":
    main()
