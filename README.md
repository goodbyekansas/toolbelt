# Toolbelt 🧰
Toolbelt is a collection of useful scripts and other things. Basically a place where we put nifty
scripts and such that could be useful to other developers.

# Installation 💾
There are two ways to install these scripts. Either by using nix-env or if you are using
home-manager to manage your nix packages.

## 1. Add toolbelt as a nix channel (not needed but recommended)

Having a nix-channel with toolbelt will make it easier to keep toolbelt up-to-date.

```
$ nix-channel --add https://github.com/goodbyekansas/toolbelt/archive/main.tar.gz toolbelt
```

followed by

```
$ nix-channel --update
```

You now have a nix-channel named `toolbelt`.

## 2. Install toolbelt

### Imperative (nix-env) 🗺️
    
If you chose to use a channel (as in 1):

```
$ nix-env --install -A toolbelt
```

If you did not want to use a channel:

```
$ nix-env --install -f https://github.com/goodbyekansas/toolbelt/tarball/main`
```

### Through home manager 🏠
    
Add a dependency to the git repo through your nix home file.

If you chose to use a channel (as in 1):

```nix
# home.nix

let
  toolbelt = import <toolbelt> {};
  # ...
in
# ...
home.packages = [
  # ...
  toolbelt
  # ...
];
```

If you did not want to use a channel:

```nix
# home.nix
let
  toolbelt = import (builtins.fetchTarball https://github.com/goodbyekansas/toolbelt/tarball/main) {};
  ...
in
...
home.packages = [ .. toolbelt .. ];
```

followed by a `home-manager switch`.

# Updating ⬆️

## With nix-env

If you use a channel to track toolbelt:

```
$ nix-channel --update toolbelt
$ nix-env --upgrade -A toolbelt --always
```

If you do not use a channel:

```
$ nix-env --install -f https://github.com/goodbyekansas/toolbelt/tarball/main`
```

## With home-manager

If you use a channel to track toolbelt:

```
$ nix-channel --update toolbelt
$ home-manager switch
```

If you do not use a channel:

It will automatically be updated whenever you run `home-manager switch`,

# Usage

## Available commands

`toolbelt` is a convenience command to inspect the collection of installed scripts, use `--help` to see what it can do.

## Authoring scripts
Put a file with a proper shebang inside the scripts folder. Note that you can use
[nix-shell shebangs](https://nixos.org/manual/nix/unstable/command-ref/nix-shell.html#use-as-a--interpreter)
to write scripts in python
for example: 
```python
#! /usr/bin/env nix-shell
#! nix-shell -i python -p python pythonPackages.prettytable

import prettytable

# Print a simple table.
t = prettytable.PrettyTable(["N", "N^2"])
for n in range(1, 10): t.add_row([n, n * n])
print t
```

### Generating man pages

Just drop a .md file next to the script with the same name and it will be generated.
