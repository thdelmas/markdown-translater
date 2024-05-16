#!/bin/bash

# Function to translate a file
translate_file() {
    local original_file=$1
    local translation_file=$2
    local target_language=$3
    "$(dirname $0)"/translater.py "$original_file" "$translation_file" --source_language en --target_language "$target_language"
}

# Check if a directory parameter is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Assign the provided directory to a variable
directory=$1

# Ensure the directory exists
if [ ! -d "$directory" ]; then
    echo "Directory $directory does not exist."
    exit 1
fi

# List of target languages
languages=("eu" "es" "fr" "ca")

# Find all .md files in the directory and subdirectories
find "$directory" -type f -name "*.md" | while read -r file; do
    # Skip if the file is a translation file (e.g., file.xx.md)
    if [[ "$file" =~ \.[a-z]{2}\.md$ ]]; then
        echo "Ignoring translation file $file."
        continue
    fi
    
    original_file="$file"
    echo "Processing original file $original_file."
    
    for lang in "${languages[@]}"; do
        translation_file="${file%.md}.$lang.md"
        
        # Check if the translation exists
        if [ -f "$translation_file" ]; then
            # Check if the translation is older than the original
            if [ "$original_file" -nt "$translation_file" ]; then
                echo "Translation $translation_file is older than the original $original_file. Translating..."
                translate_file "$original_file" "$translation_file" "$lang"
            else
                echo "Translation $translation_file is up-to-date."
            fi
        else
            echo "Translation $translation_file does not exist. Translating..."
            translate_file "$original_file" "$translation_file" "$lang"
        fi
    done
done

