alias sbf='stack build --fast'
alias rms='make run-mobility-stack'
alias backend='cd /Users/juspay/nammayatri/Backend'
alias kernel='/Users/juspay/shared-kernel'
alias server-cold-start='sh /Users/juspay/.oh-my-zsh/custom/server-start.sh'
alias loadtest='cd /Users/juspay/nammayatri-loadtest'
alias make-driver='python3 /Users/juspay/.oh-my-zsh/custom/script.py --operation make-driver'
alias kill-server="lsof | grep stack | awk '{ print $2 }' | xargs kill -9"
alias custom='cd ~/.oh-my-zsh/custom/'
alias code-backend='code /Users/juspay/nammayatri/Backend'
alias code-kernel='code /Users/juspay/shared-kernel'
alias code-custom='code ~/.oh-my-zsh/custom/'
alias nbn='nix build .#nammayatri'
alias gl='git pull'
alias gsta='git stash'
alias gstaa='git stash apply'
alias gb='git branch'
alias gco='git checkout'
alias gbc='git checkout -b'