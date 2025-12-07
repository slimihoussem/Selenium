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
                    print(f"✅ Produit '{product_name}' ajouté au panier")



if __name__ == "__main__":
    driver = open_chrome()
    test_connection("standard_user","secret_sauce",driver,"pass")
    #list_products(driver,"inventory_item_name")
    #products_elements= get_all_elements(driver,"inventory_item_img",By.CLASS_NAME)
    #img_src = [img.get_attribute('src') for img in products_elements if img.get_attribute('src')]
    #print(img_src)

    #print(check_duplicates([1,1,2,3,5,7,3]))
    select_Product(driver,"Sauce Labs Bike Light")
    time.sleep(2)

    close_chrome(driver)