"""Lightweight HTML checks for the published portfolio and demo pages."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "index.html", *sorted((ROOT / "demos").glob("*/index.html"))]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.fragments = []
        self.viewport = False
        self.title = ""
        self.in_title = False
        self.local_references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        href = attrs.get("href", "")
        for name in ("href", "src", "poster"):
            value = attrs.get(name)
            if value:
                self.local_references.append(value)
        if href.startswith("#") and href != "#":
            self.fragments.append(href[1:])
        if tag == "meta" and attrs.get("name", "").lower() == "viewport":
            self.viewport = True
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check_page(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    problems = []

    if not parser.title.strip():
        problems.append("missing page title")
    if not parser.viewport:
        problems.append("missing viewport meta")

    duplicates = sorted(name for name, count in Counter(parser.ids).items() if count > 1)
    if duplicates:
        problems.append("duplicate IDs: " + ", ".join(duplicates))

    broken = sorted(set(parser.fragments) - set(parser.ids))
    if broken:
        problems.append("broken same-page anchors: " + ", ".join(broken))

    # GitHub Pages hosts this project under /gonzalo/. Validate local assets
    # and links relative to the page, independently of external services.
    for reference in parser.local_references:
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        if parsed.path.startswith("/"):
            problems.append("root-relative path may fail on project Pages: " + reference)
            continue
        candidate = (path.parent / unquote(parsed.path)).resolve()
        if not candidate.is_relative_to(ROOT.resolve()):
            problems.append("path escapes published site: " + reference)
            continue
        if candidate.is_dir():
            candidate = candidate / "index.html"
        if not candidate.is_file():
            problems.append("missing local reference: " + reference)
    return problems


def main():
    if len(PAGES) < 20:
        raise SystemExit("Expected main site plus at least 19 demo pages")

    errors = []
    for path in PAGES:
        for problem in check_page(path):
            errors.append(f"{path.relative_to(ROOT)}: {problem}")
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(f"HTML checks passed for {len(PAGES)} pages")


if __name__ == "__main__":
    main()
