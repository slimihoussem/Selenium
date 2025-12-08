from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

# Configuration
#URL = "https://www.saucedemo.com/"
#USERNAME = "standard_user"
#PASSWORD = "secret_sauce"

def open_chrome():
    # creer une instance du navigateur avec chrome-win64 and chromedriver-win64
    chrome_binary = Path.home() / "Downloads" / "chrome-win64" / "chrome-win64" / "chrome.exe"
    driver_binary = Path.home() / "Downloads" / "chromedriver-win64" / "chromedriver-win64" / "chromedriver.exe"
    chrome_options = Options()
    prefs = {
    # Désactiver le gestionnaire de mots de passe
    "profile.password_manager_enabled": False,
    "credentials_enable_service": False
    }
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.binary_location = str(chrome_binary)
    service = Service(executable_path=str(driver_binary))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def close_chrome(driver):
    #fermer chrome
    # Fermer le navigateur
    driver.quit()
    

def test_connection(USERNAME,PASSWORD,driver,pass_or_fail="pass",):

    print(f"user           : '{USERNAME}', \npassword       : '{PASSWORD}', \nexpected result: '{pass_or_fail}'")
    expected_status = pass_or_fail
    status_tested = "pass_or_fail"

    # Créer une instance du navigateur (Chrome)
    #driver = webdriver.Chrome()  

    try:
        # Accéder au site
        driver.get("https://www.saucedemo.com/")
        #print("Page chargée :", driver.title)
    
        # Remplir le formulaire de connexion
        # Trouver le champ username et saisir les données
        username_field = driver.find_element(By.ID, "user-name")
        username_field.clear()
        username_field.send_keys(USERNAME.replace(" ",""))
    
        # Trouver le champ password et saisir les données
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(PASSWORD)
    
        # Soumettre le formulaire
        login_button = driver.find_element(By.ID, "login-button")

        start_time = time.perf_counter()
        login_button.click()

    
        # Attendre que la page se charge
        #time.sleep(2)
    
        # Test WebDriverWait function
        #WebDriverWait(driver,2).until(EC.presence_of_element_located((By.ID,"shopping_cart_container")))
        #WebDriverWait(driver,2 ).until(EC.presence_of_element_located((By.ID,"login-button")))

        end_time = time.perf_counter()
        print("time of login: ",round(end_time-start_time,2))

        # Vérifier la connexion réussie
        current_url = driver.current_url
        if "inventory" in current_url:
            print("✅ Connexion réussie!")
            #print("Page actuelle :", driver.current_url)
        
            # Afficher le titre de la page produits
            title = driver.find_element(By.CLASS_NAME, "title")
            #print("Titre de la page :", title.text)
        
            # Prendre une capture d'écran
            driver.save_screenshot("saucedemo_connected.png")
            #print("📸 Capture d'écran sauvegardée")

            status_tested="pass"
        else:
            print("❌ Échec de la connexion")
            status_tested="fail"
        
    except TimeoutException as ex:
        print("⛔ Timeout error: ", ex)

    except Exception as e:
        print("⛔ Error: ", e)

    #finally:
        # Attendre un moment pour voir le résultat
        #time.sleep(3)
    

        #print("Navigateur fermé")

    if(expected_status==status_tested):
        print("✅ ✅ ✅ Test case succes")
        return True
    else:
        print("❌ ❌ ❌ Test case fail")
        return False


# ------ test function ------  param => user, pass, status(fail or pass)
if __name__ == "__main__":
    driver = open_chrome()
    test_connection("performance_glitch_user","secret_sauce",driver,"pass")
    test_connection("","",driver)
    test_connection("standard_user","secret_sauce",driver,"fail")
    #close_chrome(driver)
