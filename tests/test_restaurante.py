#Prueba de Menu/Restaurante - Ver platos y toggle formularios
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
    time.sleep(2)

    #Ir al restaurante
    driver.get(f"{BASE_URL}/restaurante")
    time.sleep(2)

    #Verificar que hay platos
    platos = driver.find_elements(By.CSS_SELECTOR, ".card")
    if len(platos) > 0:
        print(f"[PASS] Menu carga correctamente ({len(platos)} platos)")
    else:
        print("[FAIL] No se encontraron platos en el menu")

    #Toggle primer formulario de pedido
    botones = driver.find_elements(By.CSS_SELECTOR, ".btn-order")
    if len(botones) > 0:
        botones[0].click()
        time.sleep(1)
        formularios = driver.find_elements(By.CSS_SELECTOR, ".order-form.active")
        if len(formularios) > 0:
            print("[PASS] Toggle de formulario funciona")
        else:
            print("[FAIL] Toggle de formulario no funciona")
    else:
        print("[SKIP] No hay botones de ordenar para probar toggle")

    driver.quit()

if __name__ == "__main__":
    main()


