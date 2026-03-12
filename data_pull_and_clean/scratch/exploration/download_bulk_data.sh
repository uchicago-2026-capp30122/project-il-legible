#!/usr/bin/env bash

set -euo pipefail

# ===== CONFIG =====
URLS_FILE="bulk_data_urls.csv"        # one URL per line
TARGET_DIR="data"           # existing base directory
TMP_DIR="$(mktemp -d)"       # temp working directory
# ==================

mkdir -p "$TARGET_DIR"

while IFS= read -r url; do
  [[ -z "$url" ]] && continue

  echo "Downloading: $url"

  zip_file="$TMP_DIR/$(basename "$url")"
  unzip_dir="$TMP_DIR/unzipped"

  mkdir -p "$unzip_dir"

  curl -L --fail "$url" -o "$zip_file"

  echo "Unzipping: $zip_file"
  unzip -q "$zip_file" -d "$unzip_dir"

  echo "Merging contents into $TARGET_DIR"
  rsync -av "$unzip_dir"/ "$TARGET_DIR"/

  rm -rf "$unzip_dir" "$zip_file"

done < "$URLS_FILE"

rm -rf "$TMP_DIR"

echo "All downloads merged successfully."
