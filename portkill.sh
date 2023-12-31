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
    printf "Killing all servers"
    echo " "
    echo " "
    echo "+$separator+"
    echo " "
    echo "   $quote"
    echo " "
    echo "+$separator+"
    echo " "
}

banner "Killing All Servers"

PORTS=(8013 8014 8015 8016 8017 8018 8019 8020 8023 8024 8025 8032 8050 8051 8053 8055 8099 8115 4545 6235 4343 8051)

for PORT in "${PORTS[@]}"; do
  echo "[+] Killing processes on port $PORT"
  lsof -i :$PORT | awk 'NR!=1 {print $2}' | xargs kill -9 >/dev/null 2>&1
done

