{ pkgs ? import <nixpkgs> { } }:
let
  components = {
    gitHooks = pkgs.callPackage ./git-hooks { };
  };

  scripts = pkgs.callPackage ./scripts { inherit pkgs components; };
in
pkgs.symlinkJoin {
  name = "toolbelt";
  paths = [ scripts ];
}
