import os
import re
import argparse
from typing import Dict

def fix_image_paths(base_dir: str):
    """
    Scans the base_dir for .md files and ensures image paths are in the format:
    ![](images/chapter_n/image_name.ext)
    where 'chapter_n' is derived from the filename of the .md file.
    """
    if not os.path.isdir(base_dir):
        print(f"Error: {base_dir} is not a valid directory.")
        return

    md_files = [f for f in os.listdir(base_dir) if f.endswith('.md')]
    
    for filename in md_files:
        # Derive the folder name from filename (e.g., 'chapter_1.md' -> 'chapter_1')
        folder = os.path.splitext(filename)[0]
        path = os.path.join(base_dir, filename)
        
        print(f"Processing {filename} (targeting folder: {folder})...")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex captures everything inside ![](images/...) 
        # and rebuilds it using the filename part only.
        def fix_img(m):
            full_path = m.group(1)
            filename_only = os.path.basename(full_path)
            return f"![](images/{folder}/{filename_only})"
        
        new_content = re.sub(r'!\[\]\(images/(.*?)\)', fix_img, content)
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  - Fixed image paths in {filename}")
        else:
            print(f"  - No changes needed for {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix image paths in technical Markdown files to match chapter-based structure.")
    parser.add_argument("dir", help="The directory containing the .md files to process")
    args = parser.parse_args()
    
    fix_image_paths(args.dir)
    print("Done fixing paths.")
