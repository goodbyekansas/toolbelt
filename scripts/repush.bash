#! /usr/bin/env bash

git add .
git commit --amend --no-edit
git push --force-with-lease
