from userConnection import test_connection, open_chrome, close_chrome
import json
import time 

driver = file_name = "Selenium/selenium_scripts/testCaseConnection.json"

open_chrome
try:
    start_global_time = time.perf_counter()
    with open(file_name, mode="r", encoding="utf-8") as file:
        lecteur = json.load(file)
    for data in lecteur["test_cases"]:
        
        print("-"*20)
        start_time = time.perf_counter()
        test_connection(data["username"],data["password"],driver,data["expected_result"])
        end_time = time.perf_counter()
        print(f"time execution of this case: {round(end_time-start_time,2)}s\n")

    print("\n")
    print("*"*20)
    end_global_time  = time.perf_counter()
    print(f"time execution if all cases: {round(end_global_time-start_global_time,2)}s\n")


except Exception as err:
    print("Load fail: ",err)

close_chrome(driver)
