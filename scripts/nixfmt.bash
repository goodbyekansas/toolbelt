#! /usr/bin/env nix-shell
#! nix-shell -i bash -p nixpkgs-fmt
# shellcheck shell=bash

nixpkgs-fmt .
