#Prueba de Login valido e invalido
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

    #Login valido con admin
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    email_field = driver.find_element(By.ID, "email")
    email_field.clear()
    email_field.send_keys(ADMIN_EMAIL)
    pass_field = driver.find_element(By.ID, "password")
    pass_field.clear()
    pass_field.send_keys(ADMIN_PASSWORD)
    
    # Debug: print values before submit
    print(f"  -> Email value: [{email_field.get_attribute('value')}]")
    print(f"  -> Pass value: [{pass_field.get_attribute('value')}]")
    
    # Submit form via JavaScript
    driver.execute_script("document.querySelector('form').submit()")
    time.sleep(3)

    print(f"  -> URL: {driver.current_url}")

    if "/restaurante" in driver.current_url or "/change_password" in driver.current_url:
        print("[PASS] Login valido con admin")
        if "/change_password" in driver.current_url:
            driver.find_element(By.ID, "current_password").send_keys(ADMIN_PASSWORD)
            driver.find_element(By.ID, "new_password").send_keys(ADMIN_PASSWORD)
            driver.find_element(By.ID, "confirm_password").send_keys(ADMIN_PASSWORD)
            driver.execute_script("document.querySelector('form').submit()")
            time.sleep(2)
    else:
        flashes = driver.find_elements(By.CSS_SELECTOR, ".flash")
        for f in flashes:
            print(f"  -> Flash: {f.text}")
        print("[FAIL] Login valido con admin")

    #Logout
    driver.get(f"{BASE_URL}/logout")
    time.sleep(2)

    #Login invalido
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys("wrong@email.com")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.execute_script("document.querySelector('form').submit()")
    time.sleep(2)

    if "/login" in driver.current_url:
        print("[PASS] Login invalido redirige a /login")
    else:
        print("[FAIL] Login invalido no redirige a /login")

    driver.quit()

if __name__ == "__main__":
    main()