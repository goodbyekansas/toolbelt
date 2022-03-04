{ pkgs }:
pkgs.stdenv.mkDerivation rec {
  name = "git-hooks";
  builder = builtins.toFile "builder.sh" ''
    source $stdenv/setup
    mkdir -p $out/share/git/
    cp -r ${./hooks} $out/share/git/hooks
  '';
}
