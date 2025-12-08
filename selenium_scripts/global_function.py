from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from userConnection import test_connection, open_chrome, close_chrome
from collections import Counter
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def list_products(driver,query):
    try:
        print(f"\nList Products '{query}': ")
        # trouver l'elements de la classe 'classe_name'
        list = driver.find_elements(By.CLASS_NAME,query)
        j = 1
        for i in list:
            # afficher la liste des elements
            print(f"{j} : {i.get_attribute("textContent")}")
            j+=1
        print("\n")
        

    except TimeoutException as ex:
        print("⛔ Timeout error: ", ex)

    except Exception as e:
        print("⛔ Error: ", e)

def get_all_elements(driver,Query,queryType):
    """
    Récupère tous les produits sur saucedemo.com
    
    Args:
        driver: instance du WebDriver Selenium
        Query: la valeur du sélecteur (ex: "inventory_item_name")
        queryType: le type de localisation Selenium (ex: By.CLASS_NAME)
    
    Returns:
        list: Liste des noms des produits
    """
    # Récupérer tous les éléments correspondant au Query
    Web_elements = driver.find_elements(queryType, Query)
    return Web_elements

def check_duplicates(list):
    counts = Counter(list)
    seen = set()
    duplicates_in_order = []
    for x in list:
        if counts[x] > 1 and x not in duplicates_in_order:
            duplicates_in_order.append(x)
            seen.add(x)
    return duplicates_in_order

def select_Product(driver,product_name):
    products_elements =  get_all_elements(driver,"inventory_item", By.CLASS_NAME)
    for products in products_elements:
        current_product =  get_all_elements(products,"inventory_item_name", By.CLASS_NAME)
        for current_product_name in current_product:
            if current_product_name.text == product_name:
                # Trouver le bouton "Add to cart"
                button = products.find_element(By.TAG_NAME, "button")
                # Vérifier si le produit n'est pas déjà sélectionné
                if button.text.lower() == "add to cart":
                    button.click()
                    time.sleep(0.5)
                    try:
                        button = products.find_element(By.TAG_NAME, "button")
                        # Vérifier que le clic a fonctionné en contrôlant le texte du bouton
                        if button.text.lower() == "remove":
                            print(f"✅ Produit '{product_name}' ajouté au panier")
                        else:
                            print(f"⛔ Erreur: Le clic sur '{product_name}' n'a pas fonctionné")
                    except Exception as e:
                        print("⛔ Error: ", e)

def deselect_Product(driver,product_name):
    products_elements =  get_all_elements(driver,"inventory_item", By.CLASS_NAME)
    for products in products_elements:
        current_product =  get_all_elements(products,"inventory_item_name", By.CLASS_NAME)
        for current_product_name in current_product:
            if current_product_name.text == product_name:
                # Trouver le bouton "Remove"
                button = products.find_element(By.TAG_NAME, "button")
                # Vérifier si le produit est déjà sélectionné
                if button.text.lower() == "remove":
                    button.click()
                    time.sleep(0.5)
                    try:
                        button = products.find_element(By.TAG_NAME, "button")
                        # Vérifier que le clic a fonctionné en contrôlant le texte du bouton
                        if button.text.lower() == "add to cart":
                            print(f"✅ Produit '{product_name}' retiré du panier")
                        else:
                            print(f"⛔ Erreur: Le clic sur '{product_name}' n'a pas fonctionné")
                    except Exception as e:
                        print("⛔ Error: ", e)

def checkout_with_verification(driver, expected_products):
    """
    Clique sur le panier, vérifie les produits et clique sur checkout
    
    Args:
        driver: instance du WebDriver Selenium
        expected_products: liste des noms des produits attendus dans le panier
    
    Returns:
        bool: True si la vérification est réussie et checkout lancé, False sinon
    """
    try:
        # Cliquer sur le panier (shopping cart)
        shopping_cart = driver.find_element(By.ID, "shopping_cart_container")
        shopping_cart.click()
        time.sleep(1)
        
        # Récupérer tous les produits dans le panier
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        cart_product_names = [item.find_element(By.CLASS_NAME, "inventory_item_name").text for item in cart_items]
        
        print(f"\n📦 Produits dans le panier: {cart_product_names}")
        print(f"📦 Produits attendus: {expected_products}")
        
        # Vérifier si tous les produits attendus sont présents
        all_products_match = True
        for expected in expected_products:
            if expected not in cart_product_names:
                print(f"⛔ Produit '{expected}' introuvable dans le panier")
                all_products_match = False
            else:
                print(f"✅ Produit '{expected}' trouvé dans le panier")
        
        if not all_products_match:
            print("⛔ Erreur: Tous les produits attendus ne sont pas dans le panier\n")
            return False
        
        # Vérifier qu'il n'y a pas de produits supplémentaires
        if len(cart_product_names) != len(expected_products):
            print(f"⛔ Erreur: Nombre de produits incorrect (attendu: {len(expected_products)}, trouvé: {len(cart_product_names)})\n")
            return False
        
        print("✅ Tous les produits sont correctement dans le panier")
        
        # Cliquer sur le bouton Checkout
        checkout_button = driver.find_element(By.ID, "checkout")
        checkout_button.click()
        time.sleep(1)
        
        print("✅ Bouton Checkout cliqué avec succès\n")
        return True
        
    except Exception as e:
        print(f"⛔ Erreur lors du checkout: {e}")
        return False

def achat(driver, first_name, last_name, postal_code):
    """
    Remplit le formulaire d'achat (checkout step one), vérifie les erreurs,
    clique sur Continue puis Finish, et vérifie la complétion.

    Args:
        driver: instance WebDriver
        first_name: prénom (string)
        last_name: nom (string)
        postal_code: code postal (string)

    Returns:
        bool: True si l'achat est complété avec succès, False sinon
    """
    try:
        # Remplir les champs du formulaire
        first = driver.find_element(By.ID, "first-name")
        last = driver.find_element(By.ID, "last-name")
        postal = driver.find_element(By.ID, "postal-code")

        first.clear(); first.send_keys(first_name)
        #verif_first = driver.find_element(By.ID,"first-name").get_attribute("value")
        last.clear(); last.send_keys(last_name)
        #verif_last = driver.find_element(By.ID,"last-name").get_attribute("value")
        postal.clear(); postal.send_keys(postal_code)
        #verif_postal = driver.find_element(By.ID,"postal-code").get_attribute("value")

        # Cliquer sur Continue
        continue_btn = driver.find_element(By.ID, "continue")
        continue_btn.click()
        time.sleep(0.5)

        # Vérifier la présence d'un message d'erreur sur le formulaire
        try:
            err = driver.find_element(By.CLASS_NAME, "error-message-container")
            err_text = err.text.strip()
            if err_text:
                print(f"⛔ Erreur formulaire: {err_text}")
                return False
        except Exception:
            # pas d'erreur visible
            pass

        # Sur la page de récapitulatif, cliquer sur Finish
        """
        try:
            finish_btn = driver.find_element(By.ID, "finish")
            finish_btn.click()
            time.sleep(1)

            # Vérifier la page de confirmation
            complete_header = driver.find_element(By.CLASS_NAME, "complete-header")
            if "THANK YOU" in complete_header.text.upper():
                print("✅ Achat terminé avec succès\n")
                return True
            else:
                print("⛔ Achat non terminé correctement\n")
                return False
        except Exception as e:
            print("⛔ Erreur pendant la finalisation: ", e)
            return False
        """

    except Exception as e:
        print("⛔ Erreur lors du remplissage du formulaire: ", e)
        return False

def verif_sum_price(driver,expected_products):
    """
    cart_list = driver.find_elements(By.CLASS_NAME,"cart_list")
    for p in cart_list:
        list_price_elem = get_all_elements(driver,"inventory_item_price",By.CLASS_NAME)
        #for k in list_price_elem:
        value = list_price_elem[0].get_attribute("value")
        print("get_value ",list_price_elem)
        total_price += float(value.replace("$", ""))
            
    total = driver.find_element(By.CLASS_NAME,"summary_subtotal_label").get_attribute("value").replace("$","")
    tax = driver.find_element(By.CLASS_NAME,"summary_tax_label").get_attribute("value").replace("$","")
    total_with_tax = driver.find_element(By.CLASS_NAME,"summary_total_label").get_attribute("value").replace("$","")

    if(total_price==total):
        print("calcul s7i7")
        if(total_with_tax==(total+tax)):
            print("calcul with tax s7i7")
        else:
            print("calcul with tax 8alet")
    else:
        print("calcul 8alet")
    """
    try:
        # Attendre que la page de récapitulatif soit chargée
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))

        # Récupérer les produits affichés
        overview_items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        overview_names = [item.text for item in overview_items]
        missing = [name for name in expected_products if name not in overview_names]
        if missing:
            print(f"[FAIL] Produits manquants dans le récapitulatif: {missing}")
            return False
        print(f"[PASS] Tous les produits attendus sont présents dans le récapitulatif.")

        # Récupérer les prix des produits
        price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        prices = []
        for elem in price_elements:
            try:
                price = float(elem.text.replace("$", "").replace(",", "."))
                prices.append(price)
            except Exception as e:
                print(f"[FAIL] Erreur lors de la conversion du prix: {elem.text} ({e})")
                return False
        print(prices)
        calculated_total = round(sum(prices), 2)
        print(f"Somme calculée des produits: {calculated_total}")

        # Récupérer le total affiché (hors taxes)
        summary_subtotal_elem = driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
        subtotal_text = summary_subtotal_elem.text  # Exemple: "Item total: $29.99"
        subtotal_value = float(subtotal_text.split("$")[-1].replace(",", "."))
        print(f"Total affiché (hors taxes): {subtotal_value}")

        if abs(calculated_total - subtotal_value) < 0.01:
            print("[PASS] Le total affiché correspond à la somme calculée.")
            return True
        else:
            print(f"[FAIL] Total affiché ({subtotal_value}) différent du calculé ({calculated_total})")
            return False

    except Exception as e:
        print(f"[FAIL] Erreur lors de la vérification du récapitulatif: {e}")
        return False


    


if __name__ == "__main__":
    driver = open_chrome()
    
    test_connection("standard_user","secret_sauce",driver,"pass")
    #list_products(driver,"inventory_item_name")
    #products_elements= get_all_elements(driver,"inventory_item_img",By.CLASS_NAME)
    #img_src = [img.get_attribute('src') for img in products_elements if img.get_attribute('src')]
    #print(img_src)

    #print(check_duplicates([1,1,2,3,5,7,3]))
    select_Product(driver,"Sauce Labs Bike Light")
    select_Product(driver,"Sauce Labs Backpack")
    #deselect_Product(driver,"Sauce Labs Bike Light")
    checkout_with_verification(driver,["Sauce Labs Backpack","Sauce Labs Bike Light"])
    achat(driver,"houssem","slimi","9170")
    time.sleep(2)
    verif_sum_price(driver,["Sauce Labs Backpack","Sauce Labs Bike Light"])

    close_chrome(driver) 