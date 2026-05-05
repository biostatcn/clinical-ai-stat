"""Add YAML frontmatter to all MkDocs markdown files for Decap CMS."""
import os
import re

DOCS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs"))

def has_frontmatter(content):
    return content.startswith("---")

def extract_title(content):
    """Extract the first # heading as title."""
    m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else None

def add_frontmatter(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if has_frontmatter(content):
        return False  # already has frontmatter

    title = extract_title(content)
    if not title:
        return False

    frontmatter = f"---\ntitle: \"{title}\"\n---\n\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)
    return True

def main():
    root = os.path.abspath(DOCS_DIR)
    count = 0
    for dirpath, _, files in os.walk(root):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            # Skip admin dir (already handled)
            if os.path.basename(os.path.dirname(dirpath)) == "admin" or "admin" in dirpath:
                continue
            filepath = os.path.join(dirpath, fname)
            if add_frontmatter(filepath):
                rel = os.path.relpath(filepath, root)
                print(f"  + {rel}")
                count += 1
    print(f"\nDone: {count} files updated with frontmatter.")

if __name__ == "__main__":
    main()
