# copy paste in your zshrc file 

#!/bin/bash

# Specify the aliases

magic_root="/Users/juspay/NammaYatriMagic"
project_root=""

aliases=(
    "register='python3 /Users/juspay/NammaYatriMagic/register-driver.py'"
    "random-ride='sh /Users/juspay/NammaYatriMagic/random-ride.sh'"
    "replace-driver='python3 /Users/juspay/NammaYatriMagic/replace-number.py'"
)

# Append aliases to the .zshrc file
echo "=== Setting up aliases ==="
for alias in "${aliases[@]}"; do
    echo "[+] set $alias"
    echo "alias $alias" >> ~/.zshrc
done
