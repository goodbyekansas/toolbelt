{ pkgs, components }:
pkgs.stdenv.mkDerivation (components // rec {
  name = "scripts";

  nativeBuildInputs = [ pkgs.pandoc pkgs.installShellFiles ];
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

    shopt -s extglob
    shopt -s globstar
    shopt -s nullglob

    for f in $src/**/*.!(md); do
        filename=$(basename -- "$f")
        filename="''${filename%.*}"

        filePath=$out/bin/$filename
        substituteAll $f $filePath
        chmod +x $filePath
        patchShebangs $filePath

        if [ -f "$src/$filename.md" ]; then
          pandoc -s -t man "$src/$filename.md" -o "$filename.1"
          echo "Built man page for $filename"
          installManPage "$filename.1"
        fi
    done
    compressManPages $out
  '';
})
