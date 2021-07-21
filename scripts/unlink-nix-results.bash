num=$(find . -name "result*" -type l -lname "/nix/store/*" -prune -print | grep -c /)
find . -name "result*" -type l -lname "/nix/store/*" -exec unlink {} \;
echo "Unlinked $num symlinks!"
