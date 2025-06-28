import os
from pathlib import Path
from datetime import datetime
import re
import urllib.parse

# --- Config ---
STACK_DIR = "../2blog/content/0stack"
OUTPUT_HTML = "index.html"
BASE_URL = "https://awestover.github.io/thoughts/0stack/"
THUMBNAIL_PATH = "img.jpg"  # Same for every post

# --- HTML Templates ---
HEADER = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Alek Thoughts</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="blog-index">
    <h1>A Few of <a href="https://awestover.github.io">Alek</a>'s <a href="https://awestover.github.io/thoughts">Thoughts</a></h1>
"""

FOOTER = """
  </div>
</body>
</html>
"""

def convert_markdown_links(text):
    """Convert markdown links [text](url) to HTML links."""
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.sub(pattern, r'<a href="\2">\1</a>', text)

def format_filename_for_url(filename):
    """Format filename for URL by removing extension, replacing spaces with hyphens, and escaping."""
    # Remove .md or .html extension
    name = Path(filename).stem
    
    # Replace spaces with hyphens
    name = name.replace(' ', '-')
    
    # URL encode the result
    return urllib.parse.quote(name)

def extract_description(filepath, max_lines=1):
    """Return the first few non-empty lines of a markdown file as a string."""
    lines = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)
            if len(lines) >= max_lines:
                break
    text = " ".join(lines)
    return convert_markdown_links(text)

def format_date(timestamp):
    """Format timestamp as a readable date string."""
    return datetime.fromtimestamp(timestamp).strftime("%B %d, %Y")

def generate_post_html(filename, description, date_str):
    name = Path(filename).stem
    url_filename = format_filename_for_url(filename)
    url = BASE_URL + url_filename

    html = '<div class="post">\n'
    html += f'  <img class="thumb" src="{THUMBNAIL_PATH}" alt="{name} thumbnail">\n'
    html += '  <div class="info">\n'
    html += f'    <a href="{url}">{name}</a>\n'
    html += f'    <div class="date">({date_str})</div>\n'
    if description:
        html += f'    <p>{description}</p>\n'
    html += '  </div>\n</div>\n'

    return html

def main():
    files = []
    for f in os.listdir(STACK_DIR):
        if f.endswith(".md") or f.endswith(".html"):
            full_path = os.path.join(STACK_DIR, f)
            mtime = os.path.getmtime(full_path)
            files.append((f, mtime))

    files.sort(key=lambda x: x[1], reverse=True)

    html_parts = [HEADER]
    for filename, mtime in files:
        full_path = os.path.join(STACK_DIR, filename)
        description = extract_description(full_path)
        date_str = format_date(mtime)
        html_parts.append(generate_post_html(filename, description, date_str))
    html_parts.append(FOOTER)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    print(f"✅ Wrote index to {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
