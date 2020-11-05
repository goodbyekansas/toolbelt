#! /usr/bin/env nix-shell
#! nix-shell -i bash -p niv
# shellcheck shell=bash

repos=()
extraargs=""
for arg in "$@"; do
    if [[ $arg == -* ]]; then
        extraargs="$extraargs $arg"
    else
        repos+=("$arg")
    fi
done
if [[ -z ${repos[*]} ]]; then
    echo "niv update$extraargs"
    niv "update$extraargs"
else
    command=""
    for repo in "${repos[@]}"; do
        echo "niv update $repo$extraargs"
        command="${command}niv update $repo$extraargs;"
    done
    eval "$command"
fi
