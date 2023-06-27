import json
import random
import sys



# JSON file path

json_file = "/Users/juspay/NammaYatriMagic/NammaYatri-RideBooking.json"

random_number = sys.argv[1]
customer_number = str(random.randint(1000000000, 9999999999))

# Load the JSON file
with open(json_file, 'r') as file:
    json_data = json.load(file)
    json_data["item"][0]["item"][0]["item"][0]["event"][0]["script"]["exec"][0] = f"pm.variables.set(\"driver-number\", \"{random_number}\");//data.driver.ka.numbur);"
    json_data["item"][0]["item"][1]["item"][0]["event"][0]["script"]["exec"][0] = f"pm.variables.set(\"customer-number\", \"{customer_number}\");"
    

print("[+] Customer number replaced with",customer_number)
print("[+] Driver number replaced with",random_number)

with open(json_file, 'w') as file:
    json.dump(json_data, file, indent=3)
