from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configuration
#URL = "https://www.saucedemo.com/"
#USERNAME = "standard_user"
#PASSWORD = "secret_sauce"

def test_connection(USERNAME,PASSWORD,pass_or_fail="pass"):

    print(f"user: '{USERNAME}', password: '{PASSWORD}', expected result: '{pass_or_fail}'")
    expected_status = pass_or_fail
    status_tested = pass_or_fail

    # Créer une instance du navigateur (Chrome)
    driver = webdriver.Chrome()  # Assurez-vous d'avoir chromedriver installé

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
        login_button.click()
    
        # Attendre que la page se charge
        time.sleep(2)
    
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
        
    except Exception as e:
        print("Une erreur est survenue :", str(e))
    
    finally:
        # Attendre un moment pour voir le résultat
        time.sleep(3)
    
        # Fermer le navigateur
        driver.quit()
        #print("Navigateur fermé")

    if(expected_status==status_tested):
        print("✅ ✅ ✅ Test case succes")
        return True
    else:
        print("❌ ❌ ❌ Test case fail")
        return False



# ------ test function ------  param => user, pass, status(fail or pass)
if __name__ == "__main__":
    test_connection("standard_user","secret_sauce","pass")
    test_connection("standard_user ","secret_sauce","fail")
    test_connection("","")
