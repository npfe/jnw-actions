#!/usr/bin/env python3
"""Insert a PDF download link into a Jekyll index.md, just above the first
GitHub Actions workflow badge. Idempotent: if the link is already present,
the file is left unchanged."""
import sys
import re

MARKER = "<!-- pdf-link -->"


def main():
    if len(sys.argv) != 3:
        print("usage: insert_pdf_link.py <index.md> <pdf-relative-path>", file=sys.stderr)
        sys.exit(2)
    index_path, pdf_rel = sys.argv[1], sys.argv[2]
    try:
        with open(index_path) as f:
            text = f.read()
    except FileNotFoundError:
        print(f"WARNING: {index_path} not found; skipping PDF link insertion")
        return

    if MARKER in text:
        return  # already inserted

    snippet = f"{MARKER}\n[Download PDF]({pdf_rel})\n\n"

    lines = text.split("\n")
    insert_at = None
    badge_re = re.compile(r"/actions/workflows/")
    for i, line in enumerate(lines):
        if badge_re.search(line):
            insert_at = i
            break

    if insert_at is None:
        # No workflow badge — append after frontmatter (or at top if none).
        if lines and lines[0].strip() == "---":
            for j in range(1, len(lines)):
                if lines[j].strip() == "---":
                    insert_at = j + 1
                    break
        if insert_at is None:
            insert_at = 0

    lines.insert(insert_at, snippet.rstrip("\n") + "\n")
    with open(index_path, "w") as f:
        f.write("\n".join(lines))



if __name__ == "__main__":
    main()
