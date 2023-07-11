#!/bin/bash

# Generate a random 10-digit number
random_number=$(shuf -i 1000000000-9999999999 -n 1)

echo "[+] Driver number is $random_number"
python3 /Users/juspay/NammaYatriMagic/replace-number.py $random_number
python3 /Users/juspay/NammaYatriMagic/register-driver.py $random_number