#!/bin/bash
PDF_PATH="/Volumes/Elements/HDD3-Volume-III/HDD3-Volume Ill - Advanced Receiver Design.pdf"
MINERU_BIN="/opt/homebrew/Caskroom/miniforge/base/bin/mineru"
SOURCE_DIR="/Volumes/Elements/HDD3-Volume-III/source_final"
IMAGES_DIR="/Volumes/Elements/HDD3-Volume-III/images"

mkdir -p "$SOURCE_DIR"
mkdir -p "$IMAGES_DIR"

RANGES=(
"chapter_1|5|20"
"chapter_2|21|68"
"chapter_3|69|110"
"chapter_4|111|158"
"chapter_5|159|198"
"chapter_6|199|232"
"chapter_7|233|266"
"chapter_8|267|309"
"appendices|311|331"
)

for range in "${RANGES[@]}"; do
    IFS='|' read -r id start end <<< "$range"
    echo "Processing $id (Pages $start to $end)..."
    TMP_DIR="tmp_$id"
    mkdir -p "$TMP_DIR"
    $MINERU_BIN -p "$PDF_PATH" -o "$TMP_DIR" -s "$start" -e "$end" -l th -f True
    MD_FILE=$(find "$TMP_DIR" -name "*.md" | head -n 1)
    if [ -n "$MD_FILE" ]; then
        cp "$MD_FILE" "$SOURCE_DIR/$id.md"
        echo "  - Saved $id.md"
    fi
    IMG_SRC=$(find "$TMP_DIR" -type d -name "images" | head -n 1)
    if [ -n "$IMG_SRC" ]; then
        mkdir -p "$IMAGES_DIR/$id"
        cp -R "$IMG_SRC"/* "$IMAGES_DIR/$id/"
        echo "  - Saved images to $IMAGES_DIR/$id"
    fi
    rm -rf "$TMP_DIR"
done
echo "Extraction complete. Running path fix..."
python3 /Volumes/Elements/HDD3-Volume-III/.opencode/skills/technical-book-translation/scripts/fix_paths.py "$SOURCE_DIR"
