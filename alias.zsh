gl = "git pull";
code-backend="code /path/to/your/backend/repo";
code-ny="code /path/to/your/nammayatri/repo";
code-kernel="code /path/to/your/kernel/repo";
code-config="code /Users/juspay/nix-config";
svc=", run-svc";
qsvc="nix run .#arion -- up --remove-orphans -d";
sac="nix run .#arion -- down --remove-orphans";
pgadmin="nix run .#arion -- up --remove-orphans pg-admin";
qpgadmin="nix run .#arion -- up --remove-orphans -d pg-admin";
rms="sh /Users/juspay/NammaYatriMagic/start.sh";
kill-server="sh /Users/juspay/NammaYatriMagic/portkill.sh";
gsta="git stash --include-untracked";
gstaa="git stash apply";
gb="git branch";
gco="git checkout";
gbc="git checkout -b";
backend="cd /path/to/your/nammayatri/repo";
other-backend="cd /path/to/your/other/Backend/repo";
da="direnv allow";
cc="cabal clean";
cba="cabal build all";
kernel="cd /path/to/your/kernel/repo";
ny="cd /path/to/your/other/nammayatri/repo";
".."="cd ..";
server-cold-start="sh /Users/juspay/NammaYatriMagic/server-start.sh";
prune="git gc --prune=now";
gprom="git pull --rebase origin main";
cdh="cd ~";
run-ride="newman run /Users/juspay/NammaYatriMagic/NammaYatri-RideBooking.json";
gpro="git pull --rebase origin";
flushall="sh /Users/juspay/NammaYatriMagic/flushall.sh";
run-server="nix run .#run-mobility-stack-dev";
build-rider="cabal build rider-app";
repl-rider="cabal repl rider-app";
build-driver="cabal build dynamic-offer-driver-app";
repl-driver="cabal repl dynamic-offer-driver-app";
code-driver="code /path/to/your/nammayatri/repo/Backend/app/provider-platform/dynamic-offer-driver-app/";
code-other-driver="code /path/to/your/other/Backend/repo/app/provider-platform/dynamic-offer-driver-app/";
code-rider="code /path/to/your/nammayatri/repo/Backend/app/rider-platform/rider-app/";
code-other-rider="code /path/to/your/other/Backend/repo/app/rider-platform/rider-app/";
ride-flow="sh ~/NammaYatriMagic/ride-flow.sh";