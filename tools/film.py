"""
Records tools/film.html, the 90-second tour, with Chrome's own MediaRecorder (no ffmpeg needed): media/film.mp4,
or media/film.webm where this Chrome cannot write MP4, plus a poster frame, media/film.png. 1280 x 720, no sound.
Chrome's MP4 is fragmented and says nothing of its length; tools/mp4_duration.py writes the length in.

    .venv/bin/python tools/film.py
"""
import http.server
import threading
from functools import partial
from pathlib import Path

from playwright.sync_api import sync_playwright

import mp4_duration

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "media"


def main() -> None:
    # Served over http: WebCodecs and fetch() need a real origin, not file://
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/tools/film.html"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required"])
            page = browser.new_page(viewport={"width": 1280, "height": 720}, accept_downloads=True)
            page.goto(url, wait_until="networkidle")
            page.evaluate("window.ready")
            page.evaluate("window.still(3)")
            page.screenshot(path=str(OUT / "film.png"))
            with page.expect_download(timeout=180_000) as dl:
                kind = page.evaluate("window.record()")
            name = dl.value.suggested_filename
            for old in ("film.mp4", "film.webm"):
                (OUT / old).unlink(missing_ok=True)
            dl.value.save_as(OUT / name)
            browser.close()
        if name.endswith(".mp4"):
            mp4_duration.main(OUT / name)
        print(f"film: {name} ({kind}), {(OUT / name).stat().st_size / 1e6:.1f} MB")
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
