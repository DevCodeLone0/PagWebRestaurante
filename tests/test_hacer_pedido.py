#Prueba de Hacer Pedido desde formulario dedicado
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

    #Ir a hacer pedido
    driver.get(f"{BASE_URL}/hacer_pedido")
    time.sleep(2)

    #Seleccionar primer cliente disponible
    select_cliente = driver.find_element(By.ID, "cliente_id")
    opciones = select_cliente.find_elements(By.TAG_NAME, "option")
    if len(opciones) > 1:
        select_cliente.find_elements(By.TAG_NAME, "option")[1].click()
        time.sleep(1)
        print("[PASS] Cliente seleccionado")
    else:
        print("[FAIL] No hay clientes disponibles")
        driver.quit()
        return

    #Seleccionar primer plato disponible
    select_plato = driver.find_element(By.ID, "plato_id")
    opciones_plato = select_plato.find_elements(By.TAG_NAME, "option")
    if len(opciones_plato) > 1:
        select_plato.find_elements(By.TAG_NAME, "option")[1].click()
        time.sleep(1)
        print("[PASS] Plato seleccionado")
    else:
        print("[FAIL] No hay platos disponibles")
        driver.quit()
        return

    #Ingresar cantidad
    driver.find_element(By.ID, "cantidad").send_keys("2")
    time.sleep(1)

    #Enviar pedido
    driver.find_element(By.CSS_SELECTOR, "button.btn-submit").click()
    time.sleep(2)

    if "/pedidos" in driver.current_url:
        print("[PASS] Pedido creado exitosamente")
    else:
        print("[FAIL] Pedido no se pudo crear")

    driver.quit()

if __name__ == "__main__":
    main()
