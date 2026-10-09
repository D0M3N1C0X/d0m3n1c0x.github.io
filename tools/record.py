"""
Records the short loops on the portfolio page from the live sites, with the Chrome already installed.
Each scene is a list of (action, hold in ms); every action is followed by a screenshot. Pillow joins
the screenshots into an animated WebP, and the strongest frame is saved as a still for reduced motion.

    .venv/bin/python tools/record.py            # all scenes
    .venv/bin/python tools/record.py vimeo      # one scene
    .venv/bin/python tools/record.py og         # the link preview only
"""
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "media"
SIZE = (1200, 760)
WIDTH = 960                      # width of the published loop


def scroll_to(sel, offset=-24):
    return lambda p: p.evaluate(
        "([s, o]) => window.scrollTo({top: document.querySelector(s).getBoundingClientRect().top + window.scrollY + o,"
        " behavior: 'instant'})", [sel, offset])


def scroll_by(dy):
    return lambda p: p.evaluate("dy => window.scrollBy({top: dy, behavior: 'instant'})", dy)


def slide(sel, value):
    return lambda p: p.evaluate(
        "([s, v]) => { const e = document.querySelector(s); e.value = v;"
        " for (const k of ['input', 'change']) e.dispatchEvent(new Event(k, {bubbles: true})); }", [sel, value])


def click(sel):
    return lambda p: p.click(sel)


nothing = lambda p: None

SCENES = {
    # the payroll tool: load the example files, run the checks, read the flags
    "controlli": ("https://d0m3n1c0x.github.io/controlli-cedolini/strumento/", [
        (nothing, 1400),
        (click("#esempio"), 900),
        (lambda p: (p.wait_for_function("!document.querySelector('#esegui').disabled"), p.click("#esegui")), 300),
        (scroll_to("#risultati"), 2200),
        (scroll_by(380), 1600),
        (scroll_by(380), 1600),
        (scroll_to("#novembre", -140), 2400),
    ], 3),
    # the business case: move the real uplift through break-even and watch the verdict flip
    "vimeo": ("https://d0m3n1c0x.github.io/vimeo-growth-case/model/", [
        (nothing, 1600),
        (slide("#uplift", "0.004"), 1300),
        (slide("#uplift", "0.006"), 900),
        (slide("#uplift", "0.008"), 900),
        (slide("#uplift", "0.012"), 900),
        (slide("#uplift", "0.016"), 1800),
        (scroll_to("#chart", -80), 2200),
        (slide("#uplift", "0.01"), 1600),
    ], 0),
    # the flagship: from the answer to the pay gap charts and the categories that need a justification
    "kit": ("https://d0m3n1c0x.github.io/pay-transparency-readiness-kit/", [
        (nothing, 1800),
        (scroll_to("svg[aria-label^='Gende']", -150), 2400),
        (scroll_to("svg[aria-label^='Share']", -60), 2000),
        (scroll_to("svg[aria-label^='Hourl']", -150), 2600),
    ], 1),
}


def record(name: str, browser) -> None:
    url, steps, still = SCENES[name]
    page = browser.new_page(viewport={"width": SIZE[0], "height": SIZE[1]}, device_scale_factor=1,
                            color_scheme="light", reduced_motion="reduce")
    page.goto(url, wait_until="networkidle")
    frames, holds = [], []
    for action, hold in steps:
        action(page)
        page.wait_for_timeout(350)
        img = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
        frames.append(img.resize((WIDTH, round(img.height * WIDTH / img.width)), Image.LANCZOS))
        holds.append(hold)
    page.close()
    OUT.mkdir(exist_ok=True)
    frames[0].save(OUT / f"{name}.webp", save_all=True, append_images=frames[1:], duration=holds, loop=0,
                   quality=72, method=6)
    frames[still].save(OUT / f"{name}.png", optimize=True)
    print(f"{name}: {len(frames)} frames, {(OUT / f'{name}.webp').stat().st_size / 1024:.0f} KB")


def social_card(browser) -> None:
    """The link preview: the top of this page at 1200 x 630, in light mode."""
    page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1, color_scheme="light")
    page.goto((OUT.parent / "index.html").as_uri(), wait_until="networkidle")
    page.add_style_tag(content="main, footer, .links { display: none; } body { height: 630px; display: flex; align-items: center; }"
                       " header { padding: 0 48px; } .lede { font-size: 21px; }")
    page.screenshot(path=OUT / "og.png")
    page.close()
    print("og: 1200 x 630")


if __name__ == "__main__":
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        for name in sys.argv[1:] or [*SCENES, "og"]:
            social_card(browser) if name == "og" else record(name, browser)
        browser.close()
