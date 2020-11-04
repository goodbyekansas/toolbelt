#! /usr/bin/env bash

shopt -s extglob

branches=$(git for-each-ref --shell --format='%(refname:short)' refs/heads/)
dry=false
check=true

if [[ $1 == "--dry" ]]; then
    dry=true
fi

if [[ $1 == "--no-check" ]]; then
    check=false
fi

branches=${branches[*]//*(\'main\')}

if [ $dry = true ]; then
    echo "Doing a dry run!"
    for b in $branches; do
        echo "Would delete branch: $b"
    done
    exit
fi

for b in $branches; do
    if [ $check = true ]; then
        echo "Are you sure you want to delete branch $b? (y/n)"
        read -r answer
        if [ "$answer" != "y" ]; then
            continue
        fi
    fi

    git branch --list "$b"
    b="${b//\'/}"
    git branch -D "$b"
done
