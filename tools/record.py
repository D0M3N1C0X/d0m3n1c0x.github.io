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
KIT = Path.home() / "pay-transparency-readiness-kit"     # the files the payroll tool is shown loading
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
    "controlli": ("https://d0m3n1c0x.github.io/controlli-cedolini/strumento/?lang=en", [
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
    # the payroll checks in English: the example files, the flags and what to do
    "controlli-en": ("https://d0m3n1c0x.github.io/controlli-cedolini/strumento/?lang=en", [
        (nothing, 1400),
        (click("#esempio"), 900),
        (lambda p: (p.wait_for_function("!document.querySelector('#esegui').disabled"), p.click("#esegui")), 300),
        (scroll_to("#risultati"), 2200),
        (scroll_by(380), 1600),
        (scroll_by(380), 1600),
        (scroll_to("#novembre", -140), 2400),
    ], 3),
    # the people-cost simulator: a hiring freeze against the base case, then the outlook and plan, then one employee
    "wcm-sim": ("https://d0m3n1c0x.github.io/workforce-cost-model/simulator/?lang=en", [
        (nothing, 1200),
        (lambda p: (p.click("#preset button[data-p='1']"), scroll_to("#kpis", -20)(p)), 2400),
        (scroll_to("#h-mesi", -20), 2200),
        (lambda p: (p.click("#viste button[data-v='piano']"), scroll_to("#h-piano", -20)(p)), 2600),
        (lambda p: (p.click("#viste button[data-v='costo']"), scroll_to("#h-costo", -20)(p)), 2600),
    ], 3),
    # the pay range finder: one role after another
    "ads": ("https://d0m3n1c0x.github.io/equal-value-pay-ranges/ads.html", [
        (nothing, 1600),
        (lambda p: p.select_option("#country", index=1), 1400),
        (lambda p: p.select_option("#family", index=3), 1400),
        (lambda p: p.select_option("#level", index=4), 2200),
        (scroll_to("#grades", -60), 2400),
    ], 3),
    # the Eurostat explorer: the EU, then Italy and Poland
    "wpb-dash": ("https://d0m3n1c0x.github.io/where-pay-transparency-bites/dashboard/", [
        (nothing, 1800),
        (lambda p: p.select_option("select", label="Italy"), 2000),
        (lambda p: p.select_option("select", label="Poland"), 2000),
        (scroll_by(420), 2200),
    ], 1),
    # the AI Act tool: the sample systems, the register, what applies when, whom to tell
    "aiact-tool": ("https://d0m3n1c0x.github.io/ai-act-hr-readiness-kit/tool/?lang=en", [
        (nothing, 1400),
        (lambda p: (p.click("#esempio"), p.wait_for_selector("#kpis .s-kpi")), 600),
        (scroll_to("#kpis", -90), 2200),
        (scroll_to("#h-registro", -20), 2400),
        (scroll_to("#h-obblighi", -20), 2400),
        (scroll_to("#h-avvisi", -20), 2400),
    ], 2),
    # the kit's browser tool: the sample employer, the obligations, the seven items and the category screen
    # the payroll check on a full year of actual pay: payroll, role grid and pay-code map in, then the results
    "kit-tool": ("https://d0m3n1c0x.github.io/pay-transparency-readiness-kit/tool/?lang=en", [
        (nothing, 1400),
        (lambda p: (p.set_input_files("#file-paghe", str(KIT / "data" / "payroll_reference_year.csv")),
                    p.set_input_files("#file-griglia", str(KIT / "data" / "job_evaluation.csv")),
                    p.set_input_files("#file-codici", str(KIT / "web" / "template_pay_code_map.csv")),
                    p.wait_for_function("!document.querySelector('#esegui').disabled"),
                    scroll_to("#passo-colonne", -40)(p)), 2400),
        (lambda p: (p.click("#esegui"), p.wait_for_selector("#kpis .s-kpi"),
                    scroll_to("#payroll-reconciliation-result", -140)(p)), 2400),
        (scroll_to("#kpis", -90), 2400),
        (scroll_to("#grafico-categorie", -120), 2600),
        (scroll_to("#tab-categorie", -40), 2400),
    ], 3),
    # the job search: the roles worth an hour, why one scored 94, every posting with its verdict, the funnel
    "jsa": ("https://d0m3n1c0x.github.io/job-search-agent/demo/", [
        (nothing, 1600),
        (scroll_to("#todayhead", -20), 2000),
        (click("#deck button:has-text('Why this score') >> nth=0"), 3400),
        (lambda p: (p.click("#dclose"), p.click(".tab:has-text('All postings')")), 2600),
        (click(".tab:has-text('Insights')"), 2600),
    ], 2),
    # the retention check: the example file, the columns, the results section by section
    "hpa-tool": ("https://d0m3n1c0x.github.io/hr-people-analytics/tool/", [
        (nothing, 1400),
        (lambda p: (p.click("#esempio"), p.wait_for_selector("#colonne select")), 1600),
        (lambda p: (p.click("#calcola"), p.wait_for_selector("#kpis .s-kpi")), 600),
        (scroll_to("#kpis", -90), 2400),
        (scroll_to("#h-surv", -20), 2400),
        (scroll_to("#h-drv", -20), 2600),
        (scroll_to("#h-team", -20), 2600),
    ], 3),
    # the survey check: the example files, the columns, scores, drivers, teams
    "esa-tool": ("https://d0m3n1c0x.github.io/engagement-survey-analytics/tool/", [
        (nothing, 1400),
        (lambda p: (p.click("#esempio"), p.wait_for_selector("#tab-items input")), 1600),
        (lambda p: (p.click("#calcola"), p.wait_for_selector("#kpis .s-kpi")), 600),
        (scroll_to("#kpis", -90), 2600),
        (scroll_to("#tab-drv", -140), 2600),
        (scroll_to("#tab-grp", -140), 2400),
    ], 3),
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
