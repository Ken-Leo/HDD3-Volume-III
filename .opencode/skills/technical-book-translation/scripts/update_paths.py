import os
import re

base_dir = "/Volumes/Elements/HDD1-Volume-I/thai_final"
files_to_process = {
    "chapter_1.md": "chapter_1",
    "chapter_2.md": "chapter_2",
    "chapter_3.md": "chapter_3",
    "chapter_4.md": "chapter_4",
    "chapter_5.md": "chapter_5",
    "chapter_6.md": "chapter_6",
    "appendices.md": "appendices",
}

for filename, folder in files_to_process.items():
    path = os.path.join(base_dir, filename)
    if os.path.exists(path):
        print(f"Processing {filename}...")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace ![](images/ with ![](images/chapter_N/
        new_content = content.replace("![](images/", f"![](images/{folder}/")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        print(f"File {filename} not found, skipping.")

print("Done updating paths.")
