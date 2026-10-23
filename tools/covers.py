"""
Covers and social cards for the portfolio's repositories, in one visual family (brand/cover.html).

For each repository: site-assets/cover-light.png and cover-dark.png at 2x for the README (GitHub picks one with
<picture> and prefers-color-scheme), and site-assets/og.png at 1280 x 640 for link previews and GitHub's social
preview. Rendered with the Chrome already installed, so the system font is SF Pro on a Mac.

    .venv/bin/python tools/covers.py                          # every repository
    .venv/bin/python tools/covers.py pay-transparency-readiness-kit
"""
import json
import sys
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright

HOME = Path.home()
TEMPLATE = Path(__file__).resolve().parent.parent / "brand" / "cover.html"

SPECS = {
    "pay-transparency-readiness-kit": {
        "eyebrow": "EU Pay Transparency Directive · Articles 4 to 12",
        "title": "Ready for the EU Pay Transparency Directive?",
        "sub": "A four-country employer, run end to end as a consulting team would deliver it: the seven reporting "
               "items, the 5% screen, the cost of closing the gaps and the deadlines.",
        "stats": [["17.6%", "hourly gender pay gap across the group"], ["12 of 28", "categories of workers to justify or remedy"],
                  ["€1.9M", "a year, at most, to close every flagged gap"]],
        "chips": ["Python", "Excel model", "Browser tool", "Board deck"],
    },
}


def render(repo: str, spec: dict, browser) -> None:
    out = HOME / repo / "site-assets"
    out.mkdir(exist_ok=True)
    url = f"{TEMPLATE.as_uri()}?spec={quote(json.dumps({**spec, 'repo': repo}))}"
    for theme, scale, name in (("light", 2, "cover-light.png"), ("dark", 2, "cover-dark.png"), ("dark", 1, "og.png")):
        page = browser.new_page(viewport={"width": 1280, "height": 640}, device_scale_factor=scale)
        page.goto(f"{url}&theme={theme}")
        page.wait_for_timeout(300)
        page.screenshot(path=out / name)
        page.close()
    print(f"{repo}: cover-light.png, cover-dark.png, og.png")


def main() -> None:
    names = sys.argv[1:] or list(SPECS)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        for name in names:
            render(name, SPECS[name], browser)
        browser.close()


if __name__ == "__main__":
    main()
