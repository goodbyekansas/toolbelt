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
$ nix-env --update toolbelt
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
