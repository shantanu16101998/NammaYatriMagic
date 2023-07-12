import requests
import sys
import json
import pprint
import random

def driver_enabler():
    if len(sys.argv) < 2:
        print("Usage: python script.py <driver_number>")
        sys.exit(1)

    # getting admin token 
    dashboard_token = "1460d294-8c69-44b9-811a-c370949d056e"
    auth_body = {
        "mobileNumber": "9999999999",
        "mobileCountryCode": "+91",
        "merchantId": "favorit0-0000-0000-0000-00000favorit"
        }
    
    x_admin = requests.post('http://localhost:8016/ui/auth',json=auth_body)

    auth_id_admin = x_admin.json()["authId"]

    verify_body = {
            "otp": "7891",
            "deviceToken": "8e83b5dc-99a0-4306-b90d-2345f3050972"
        }
    
    y_admin = requests.post(f'http://localhost:8016/ui/auth/{auth_id_admin}/verify',json=verify_body)
    
    admin_token = y_admin.json()["token"]
    number = sys.argv[1]
    
    auth_body = {
    "mobileNumber": str(number),
    "mobileCountryCode": "+91",
    "merchantId": "favorit0-0000-0000-0000-00000favorit"
    }
    x = requests.post('http://localhost:8016/ui/auth',json=auth_body)
    print("[+] Authenticating the driver",x.json())
    auth_id = x.json()["authId"]
    verify_body = {
        "otp": "7891",
        "deviceToken": "8e83b5dc-99a0-4306-b90d-2345f3050972"
    }
    y = requests.post(f'http://localhost:8016/ui/auth/{auth_id}/verify',json=verify_body)
    print("[+] Verifying the driver")
    driverId = y.json()["person"]["id"]
    token = admin_token

    a = requests.get(f'http://localhost:8016/ui/auth/logout')
            
    z = requests.post(f'http://localhost:8016/ui/org/driver/{driverId}?enabled=true',headers={'token' : token})
    print("[+] enabling the driver",z.json())
    vehicle = {
        "variant": "AUTO_RICKSHAW",
        "color": "string",
        "size": "string",
        "vehicleClass": "3WT",
        "category": "CAR",
        "capacity": 5,
        "model": "string",
        "registrationNo": str(random.randint(1000,9999)),
        "registrationCategory": "COMMERCIAL",
        "make": "string",
        "colour": "ipsum",
        "energyType": "string",
        "driverName": "",
    }

    a = requests.post(f'http://localhost:8018/bpp/driver-offer/NAMMA_YATRI_PARTNER/driver/{driverId}/addVehicle',json=vehicle,headers={'token' : dashboard_token})
    print("[+] Adding the vehicle",a.json())
    print("")

driver_enabler()