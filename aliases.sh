# copy paste in your zshrc file 
# change juspay to your username

#!/bin/bash

# Specify the aliases
aliases=(
    "cba='cabal build all'"
    "cc='cabal clean'"
    "cdh='cd ~'"
    "code-backend='code /Users/juspay/nammayatri/Backend'"
    "code-config='code /Users/juspay/nix-config'"
    "code-custom='code ~/.oh-my-zsh/custom/'"
    "code-driver='code /Users/juspay/nammayatri/Backend/app/provider-platform/dynamic-offer-driver-app/'"
    "code-kernel='code /Users/juspay/shared-kernel'"
    "code-ny='code /Users/juspay/nammayatri/'"
    "code-other-driver='code /Users/juspay/ny/nammayatri/Backend/app/provider-platform/dynamic-offer-driver-app/'"
    "code-other-rider='code /Users/juspay/nammayatri/Backend/app/rider-platform/rider-app/'"
    "code-rider='code /Users/juspay/nammayatri/Backend/app/rider-platform/rider-app/'"
    "da='direnv allow'"
    "flushall='sh /Users/juspay/NammaYatriMagic/flushall.sh'"
    "gb='git branch'"
    "gbc='git checkout -b'"
    "gco='git checkout'"
    "gl='git pull'"
    "gpro='git pull --rebase origin'"
    "gprom='git pull --rebase origin main'"
    "gsta='git stash --include-untracked'"
    "gstaa='git stash apply'"
    "kernel='cd /Users/juspay/shared-kernel'"
    "kill-server='sh /Users/juspay/NammaYatriMagic/portkill.sh'"
    "magic='cd ~/NammaYatriMagic/'"
    "ny='cd /Users/juspay/nammayatri/'"
    "other-backend='cd /Users/juspay/ny/nammayatri/Backend'"
    "pgadmin='nix run .#arion -- up --remove-orphans pg-admin'"
    "prune='git gc --prune=now'"
    "qpgadmin='nix run .#arion -- up --remove-orphans -d pg-admin'"
    "qsvc='nix run .#arion -- up --remove-orphans -d'"
    "repl-driver='cabal repl dynamic-offer-driver-app'"
    "repl-rider='cabal repl rider-app'"
    "ride-flow='sh ~/NammaYatriMagic/ride-flow.sh'"
    "rms='sh /Users/juspay/NammaYatriMagic/start.sh'"
    "run-ride='newman run /Users/juspay/NammaYatriMagic/NammaYatri-RideBooking.json'"
    "run-server='nix run .#run-mobility-stack-dev'"
    "sac='nix run .#arion -- down --remove-orphans'"
    "server-cold-start='sh /Users/juspay/NammaYatriMagic/server-start.sh'"
    "svc=', run-svc'"
)

# Append aliases to the .zshrc file
for alias in "${aliases[@]}"; do
    echo "alias $alias" >> ~/.zshrc
done
