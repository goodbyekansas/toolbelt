{ pkgs ? import <nixpkgs> { } }:
pkgs.stdenv.mkDerivation rec {
  name = "scripts";
  src = (builtins.path {
    path = ./.;
    inherit name;
    filter =
      (
        path: type: !(type == "regular" && baseNameOf path == "default.nix")
      );
  });
  builder = builtins.toFile "builder.sh" ''
    source $stdenv/setup
    mkdir -p $out/bin

    for f in $src/*; do
        filename=$(basename -- "$f")
        filename="''${filename%.*}"

        filePath=$out/bin/$filename
        cp $f $filePath
        chmod +x $filePath
        patchShebangs $filePath
    done
  '';
}
