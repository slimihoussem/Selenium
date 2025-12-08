from userConnection import test_connection, open_chrome, close_chrome
import global_function as fn 
import json

filename = "Selenium/selenium_scripts/end_to_end_test_cases.json"


def main(file_name):
    try:
        with open(file_name, mode="r", encoding="utf-8") as file:
            lecteur = json.load(file)
        for data in lecteur["test_cases"]:
            print("description: ",data["description"])
            print("expected_order_message: ",data["expected_order_message"])
            driver = open_chrome()
            test_connection(data["username"],data["password"],driver)
            product = data["products_to_buy"]
            
            for prod in product:
                fn.select_Product(driver,prod)

            fn.checkout_with_verification(driver,product)
            checkout_info = data["checkout_info"]
            fn.achat(driver,checkout_info["first_name"],checkout_info["last_name"],checkout_info["postal_code"])
            fn.verif_sum_price(driver,product)
            close_chrome(driver)
            print("\n")
            print("*"*50)
            print("\n")

    except Exception as err:
        print("Load fail: ",err)




if __name__ == "__main__":
    main(filename)