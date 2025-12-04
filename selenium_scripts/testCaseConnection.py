from userConnection import test_connection
import json
import time 

name_file = "Selenium/selenium_scripts/testCaseConnection.json"

try:
    start_global_time = time.perf_counter()
    with open(name_file, mode="r", encoding="utf-8") as file:
        lecteur = json.load(file)
    for data in lecteur["test_cases"]:
        
        print("-"*20)
        start_time = time.perf_counter()
        test_connection(data["username"],data["password"],data["expected_result"])
        end_time = time.perf_counter()
        print(f"time execution of this case: {round(end_time-start_time,2)}s\n")

    print("\n")
    print("*"*20)
    end_global_time  = time.perf_counter()
    print(f"time execution if all cases: {round(end_global_time-start_global_time,2)}s")


except Exception as err:
    print("Load fail: ",err)
