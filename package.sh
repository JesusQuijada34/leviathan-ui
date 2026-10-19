#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
./build.sh
OUT="$ROOT/build/windows-x64"
if [ ! -f "$OUT/liblevthcore.dll" ]; then
  echo "Packaging stopped: this host has no MinGW-w64 DLL build; no Windows package was made." >&2
  exit 2
fi
mkdir -p dist
STAGE="$ROOT/build/sdk-package"
rm -rf "$STAGE"
mkdir -p "$STAGE/bin" "$STAGE/include"
cp "$OUT"/*.dll "$STAGE/bin/"
cp native/include/levth.h "$STAGE/include/"
cp app/app-icon.ico native/README.md "$STAGE/"
ARCHIVE="$ROOT/dist/Leviathan-UI-Native-SDK-1.0.5-win-x64.tar.gz"
tar -czf "$ARCHIVE" -C "$STAGE" .
echo "Package ready: $ARCHIVE"
