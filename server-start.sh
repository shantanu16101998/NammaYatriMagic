banner()
{
  echo "+----------------------------------------------------------------------------------------------+"
  echo "|  ____ ____ ____ ___ ____ ____ _ _  _ ____    ___ _  _ ____    ____ ____ ____ _  _ ____ ____  |"
  echo "|  |__/ |___ [__   |  |__| |__/ | |\ | | __     |  |__| |___    [__  |___ |__/ |  | |___ |__/  |"
  echo "|  |  \ |___ ___]  |  |  | |  \ | | \| |__]     |  |  | |___    ___] |___ |  \  \/  |___ |  \  |"
  echo "+----------------------------------------------------------------------------------------------+"
  echo ""
}

banner "Starting the server"
sleep 3

# cd /Users/juspay/nammayatri/Backend
set +x
nix run .#arion -- down --remove-orphans
nix run .#arion -- up --remove-orphans -d
nix run .#arion -- up --remove-orphans -d pg-admin
echo "Go and sleep for 45 seconds."
sleep 45
, run-mobility-stack-dev
