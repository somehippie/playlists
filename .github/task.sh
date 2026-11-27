#!/usr/bin/env bash
# Fetch Archivo (variable width and weight) as woff2, plus its licence, for self-hosting.
set -euo pipefail
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
mkdir -p out/fonts
curl -sfA "$UA" 'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap' -o out/fonts/archivo.css
grep -o 'https://fonts.gstatic.com/[^)]*' out/fonts/archivo.css | sort -u | while read -r u; do curl -sf "$u" -o "out/fonts/$(basename "$u")"; done
curl -sf https://raw.githubusercontent.com/google/fonts/main/ofl/archivo/OFL.txt -o out/fonts/OFL.txt
