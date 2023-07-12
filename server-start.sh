get_random_quote() {
    response=$(curl -s "https://zenquotes.io/api/random")
    if [ $? -eq 0 ]; then
        quote=$(echo "$response" | jq -r '.[0].q')
        author=$(echo "$response" | jq -r '.[0].a')
        echo "$quote - $author"
    else
        echo "Internet is good for your health - Shantanu Mukherjee"
    fi
}

banner() {
    quote=$(get_random_quote)
    quote_length=${#quote}
    banner_width=$((quote_length + 10))
    space=5
    quote_width=$((banner_width - 10))

    # Generate the separator line
    separator=$(printf -- '-%.0s' $(seq "$banner_width"))
    echo " "
    printf "Restarting the server"
    echo " "
    echo " "
    echo "+$separator+"
    echo " "
    echo "   $quote"
    echo " "
    echo "+$separator+"
    echo " "
}


banner
sleep 3

set +x
nix run .#arion -- down --remove-orphans
nix run .#arion -- up --remove-orphans -d
nix run .#arion -- up --remove-orphans -d pg-admin
sh /Users/juspay/NammaYatriMagic/portkill.sh
echo "Go and sleep for 45 seconds."
sleep 45
, run-mobility-stack-dev
