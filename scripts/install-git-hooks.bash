#! /usr/bin/env bash
root_path="@gitHooks@"

hooks_path="$root_path/share/git/hooks"

if ! root_repo=$(git rev-parse --show-toplevel); then
   echo "Failed to find root of the git repository."
   echo "Are you really in a git repository?"
   exit 1
fi

hook_dir="$root_repo/.git/hooks"

echo "🪝 Setting up git hooks!"
for hook in "$hooks_path"/*; do
    hook_name=$(basename "$hook")
    hook_destination="$hook_dir/$hook_name"

    if [ -e "$hook_destination" ] && [ "$1" == "--force" ]; then
        unlink "$hook_destination"
    fi

    if [ -e "$hook_destination" ]; then
        echo -e -n "\e[91m\"$hook_name\"\e[0m already exists. Overwrite? (\e[92my\e[0m/\e[91mN\e[0m): "
        read -r -n 1
        echo ""
        if [ "$REPLY" == "y" ]; then
            unlink "$hook_destination"
        fi
    fi

    if [ -e "$hook_destination" ]; then
        echo "☠️ Skipping $hook_name since you already had one in \".git/hooks\"."
    else
        ln -s "$hook" "$root_repo/.git/hooks"
        echo -e "🐟 Installed \e[94m\"$hook_name\"\e[0m."
    fi
done

echo -e "🎣 \e[32mDone setting up git hooks!\e[0m"



