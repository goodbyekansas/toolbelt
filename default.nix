{ pkgs ? import <nixpkgs> { } }:
let
  scripts = import ./scripts { inherit pkgs; };
in
pkgs.symlinkJoin {
  name = "toolbelt";
  paths = [ scripts ];
}
