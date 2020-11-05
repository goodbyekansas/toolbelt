#! /usr/bin/env nix-shell
#! nix-shell -i bash -p shellcheck

shopt -s extglob
shopt -s globstar

shellcheck ./scripts/**/*.!(nix|md)
