#! /usr/bin/env nix-shell
#! nix-shell -i bash -p bat
# shellcheck shell=bash

if [ "$1" == "--list" ]; then
    for f in "$(dirname "$(readlink -f "$0")")"/*; do
        basename "$f"
    done
elif [ "$1" == "--source" ]; then
    bat "$(dirname "$0")/$2" --language bash
elif [ "$1" == "--help" ] && [ -n "$2" ]; then
    man "$2"
elif [ "$1" == "--help" ]; then
    echo "Toolbelt 🧰 is a collection of tools
    toolbelt options:
      --list   to list commands 🔎
      --source <command>   to view its source 📜
      --help <command>   to view the man page ♂️📄 of the command, if it exists
      "
fi
