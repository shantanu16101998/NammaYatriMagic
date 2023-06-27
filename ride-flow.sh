#!bin/bash
banner()
{
    echo "+--------------------------------------------------------------------------------------+"
    echo "|               #                                                                      |";    
    echo "|      ###      #       #                               ####    ##                     |";
    echo "|      #  #             #                               #        #                     |";
    echo "|      #  #    ##     ###    ##                         ###      #     ##    #   #     |";
    echo "|      ###      #    #  #   # ##                        #        #    #  #   # # #     |";
    echo "|      #  #     #    #  #   ##                          #        #    #  #   # # #     |";
    echo "|      #  #    ###    ###    ###                        #       ###    ##     # #      |";
    echo "+--------------------------------------------------------------------------------------+"
}


banner
# change magic root here
python3 /Users/juspay/.oh-my-zsh/custom/ride-flow-comment.py
echo "[+] Killing servers"
PORTS=(8013 8014 8015 8016 8017 8018 8019 8020 8023 8024 8025 8032 8050 8051 8053 8055 8099 8115 4545 6235 4343 8051)

for PORT in "${PORTS[@]}"; do
  lsof -i :$PORT | awk 'NR!=1 {print $2}' | xargs kill -9 >/dev/null 2>&1
done
echo "All servers killed"
echo "[+] Building Rider App"
cabal build rider-app
echo "[+] Building Driver App"
cabal build dynamic-offer-driver-app
echo "[+] Building Gateway"
cabal build beckn-gateway
echo "[+] Building Mock Registry"
cabal build mock-registry
echo "[+] Building Driver Offer Allocator"
cabal build driver-offer-allocator
nix run .#run-mobility-stack-dev