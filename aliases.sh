# copy paste in your zshrc file 

#!/bin/bash

# Specify the aliases

magic_root=""
project_root=""

aliases=(
    "cba='cabal build all'"
    "cc='cabal clean'"
    "cdh='cd ~'"
    "da='direnv allow'"
    "flushall='sh $magic_root/flushall.sh'"
    "gb='git branch'"
    "gbc='git checkout -b'"
    "gco='git checkout'"
    "gl='git pull'"
    "gpro='git pull --rebase origin'"
    "gprom='git pull --rebase origin main'"
    "gsta='git stash --include-untracked'"
    "gstaa='git stash apply'"
    "kill-server='sh $magic_root/portkill.sh'"
    "magic='cd $magic_root'"
    "ny='cd $project_root'"
    "backend='cd $project_root/Backend'"
    "pgadmin='nix run .#arion -- up --remove-orphans pg-admin'"
    "prune='git gc --prune=now'"
    "qpgadmin='nix run .#arion -- up --remove-orphans -d pg-admin'"
    "qsvc='nix run .#arion -- up --remove-orphans -d'"
    "repl-driver='cabal repl dynamic-offer-driver-app'"
    "repl-rider='cabal repl rider-app'"
    "ride-flow='sh $magic_root/ride-flow.sh'"
    "rms='sh $magic_root/start.sh'"
    "run-ride='newman run $magic_root/NammaYatri-RideBooking.json'"
    "run-server='nix run .#run-mobility-stack-dev'"
    "sac='nix run .#arion -- down --remove-orphans'"
    "server-cold-start='sh $magic_root/server-start.sh'"
    "svc=', run-svc'"
)

# Append aliases to the .zshrc file
echo "=== Setting up aliases ==="
for alias in "${aliases[@]}"; do
    echo "[+] set $alias"
    # echo "alias $alias" >> ~/.zshrc
done
