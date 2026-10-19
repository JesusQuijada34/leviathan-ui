#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
OUT="$ROOT/build/windows-x64"
CC_WIN=${CC_WIN:-x86_64-w64-mingw32-gcc}
WINDRES=${WINDRES:-x86_64-w64-mingw32-windres}

if command -v "$CC_WIN" >/dev/null 2>&1 && command -v "$WINDRES" >/dev/null 2>&1; then
  mkdir -p "$OUT"
  "$WINDRES" native/resources/levth_version.rc -O coff -o "$OUT/levth_version.o"
  "$CC_WIN" -std=c11 -O2 -Wall -Wextra -DLEVTH_CORE_BUILD -Inative/include -shared \
    native/src/liblevthcore.c "$OUT/levth_version.o" -Wl,--out-implib,"$OUT/libliblevthcore.dll.a" \
    -o "$OUT/liblevthcore.dll"
  for module in setup window progressbar; do
    "$CC_WIN" -std=c11 -O2 -Wall -Wextra -DLEVTH_MODULE_BUILD -Inative/include -shared \
      "native/src/liblevth${module}.c" "$OUT/levth_version.o" -L"$OUT" -lliblevthcore \
      -ldwmapi -luser32 -o "$OUT/liblevth${module}.dll"
  done
  echo "Windows x64 DLL build complete: $OUT"
  if [ -n "${LEVTH_SIGN_CERT_SHA1:-}" ]; then
    if ! command -v signtool >/dev/null 2>&1; then
      echo "Configured certificate thumbprint, but signtool is unavailable." >&2
      exit 4
    fi
    for binary in "$OUT"/*.dll; do
      signtool sign /fd SHA256 /sha1 "$LEVTH_SIGN_CERT_SHA1" /tr https://timestamp.digicert.com /td SHA256 /d "Leviathan-UI Native Framework" "$binary"
      signtool verify /pa /all "$binary"
    done
  else
    echo "Unsigned artifacts: configure LEVTH_SIGN_CERT_SHA1 with a valid company certificate to sign."
  fi
else
  echo "MinGW-w64 cross compiler not installed; running portable native ABI tests instead."
  make -C native clean test
  echo "No Windows DLLs were produced in this Linux environment. Use build.bat on Windows or install MinGW-w64."
fi
