#!/bin/bash

# Generate a random 10-digit number
random_number=$(shuf -i 1000000000-9999999999 -n 1)

python3 /Users/juspay/NammaYatriMagic/register-driver.py $random_number

json_file="/Users/juspay/NammaYatriMagic/NammaYatri-RideBooking.json"

python3 /Users/juspay/NammaYatriMagic/replace-number.py $random_number