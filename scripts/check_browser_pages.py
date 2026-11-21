"""Smoke-test the public portfolio pages with a real browser at two widths."""

import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "index.html", *sorted((ROOT / "demos").glob("*/index.html"))]
VIEWPORTS = [(1365, 900), (390, 844)]


class LocalHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format, *args):
        pass


def main():
    assert len(PAGES) >= 20, "Not enough demo pages found"
    server = ThreadingHTTPServer(("127.0.0.1", 0), LocalHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    failures = []
    checked = 0

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                for width, height in VIEWPORTS:
                    context = browser.new_context(viewport={"width": width, "height": height})
                    for source in PAGES:
                        relative_path = source.relative_to(ROOT).as_posix()
                        url = f"http://127.0.0.1:{server.server_port}/{quote(relative_path)}"
                        page = context.new_page()
                        errors = []
                        page.on("pageerror", lambda err: errors.append(str(err)))
                        try:
                            response = page.goto(url, wait_until="domcontentloaded", timeout=20000)
                            if not response or not response.ok:
                                raise AssertionError("Document request failed")

                            page.wait_for_timeout(150)
                            if not page.title().strip():
                                raise AssertionError("Empty page title")
                            if not page.locator("h1").count():
                                raise AssertionError("Missing main heading")
                            if errors:
                                raise AssertionError("Uncaught JS exceptions: " + " | ".join(errors))

                            full_width = page.evaluate("document.documentElement.scrollWidth")
                            if full_width > width + 3:
                                raise AssertionError(
                                    f"Horizontal overflow: content {full_width}px, viewport {width}px"
                                )
                            checked += 1
                            print(f"OK {width}px {relative_path}", flush=True)
                        except Exception as exc:
                            failures.append(f"{width}px {relative_path}: {str(exc)[:330]}")
                        finally:
                            page.close()
                    context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()

    if failures:
        print("\nBrowser QA problems:")
        for failure in failures:
            print("- " + failure)
        raise SystemExit(f"{len(failures)} checks failed out of {len(PAGES)*len(VIEWPORTS)}")

    print(f"Browser QA passed: {checked} page/viewport combinations")


if __name__ == "__main__":
    main()
