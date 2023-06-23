banner()
{
  echo "+-------------------------------------------------------------------------------------+"
  echo "|  _,_ _ _,  _,  _ _, _  _,        _, _,  _,             _, __, __, _,_ __, __,  _,   |"
  echo "|  |_/ | |   |   | |\ | / _       / \ |   |             (_  |_  |_) | / |_  |_) (_    |"
  echo "|  | \ | | , | , | | \| \ /       |~| | , | ,           , ) |   | \ |/  |   | \ , )   |"
  echo "|  ~ ~ ~ ~~~ ~~~ ~ ~  ~  ~        ~ ~ ~~~ ~~~            ~  ~~~ ~ ~ ~   ~~~ ~ ~  ~    |"
  echo "+-------------------------------------------------------------------------------------+"
}

banner "Killing All Servers"

# npx kill-port 8013
# npx kill-port 8014
# npx kill-port 8015
# npx kill-port 8016
# npx kill-port 8017
# npx kill-port 8018
# npx kill-port 8019
# npx kill-port 8055
# npx kill-port 8115
# npx kill-port 8115
# npx kill-port 4545
# npx kill-port 6235
# npx kill-port 4343
# npx kill-port 8023
# npx kill-port 8051

PORTS=(8013 8014 8015 8016 8017 8018 8019 8020 8023 8024 8025 8032 8050 8051 8053 8055 8099 8115 4545 6235 4343 8051)

for PORT in "${PORTS[@]}"; do
  echo "[+] Killing processes on port $PORT"
  lsof -i :$PORT | awk 'NR!=1 {print $2}' | xargs kill -9 >/dev/null 2>&1
done

