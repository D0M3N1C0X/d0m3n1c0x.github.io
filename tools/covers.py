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
    "controlli-cedolini": {
        "eyebrow": "Payroll operations · CCNL Terziario, Italy",
        "title": "Catch payroll errors before the client does",
        "sub": "Fourteen checks on Italian payslips before they go out: minimums, seniority, social security, severance, "
               "holidays, the F24 tax payment and leavers. Recomputed from the contract's rules, not from the payroll software.",
        "stats": [["35 of 35", "planted errors found, with no false alarms"], ["14", "checks, each with its source in the agreement"],
                  ["3 engines", "Python, a live spreadsheet and a browser tool, in agreement"]],
        "chips": ["Python", "Excel and Google Sheets", "Browser tool", "Sourced rules"],
    },
    "workforce-cost-model": {
        "eyebrow": "People budget · HR and finance",
        "title": "What will next year's people cost be?",
        "sub": "A two-country employer's people budget, built as HR and finance would build it: what an employee really "
               "costs, why last year overran, and next year under your own scenarios.",
        "stats": [["€111.0M", "FY2027 in the base case, +3.6% on FY2026"], ["€5.8M", "FY2026 over budget, explained by headcount"],
                  ["€59,382", "fully loaded cost of an FTE in Milan, €41,727 in Kraków"]],
        "chips": ["Python", "Excel model", "Scenario simulator", "CFO memo"],
    },
    "equal-value-pay-ranges": {
        "eyebrow": "Reward · EU Pay Transparency Directive",
        "title": "Pay ranges that pay the job, not the family",
        "sub": "From family bands to one range per grade and country, priced on Eurostat market data, with every employee "
               "placed against it and the range to publish for every role.",
        "stats": [["74%", "gap between midpoints inside one grade of equal value"], ["€3.02M", "a year to bring 824 people to the new minimum"],
                  ["144", "role and country ranges, ready to advertise"]],
        "chips": ["Python", "Excel model", "Eurostat data", "Pay range finder"],
    },
    "vimeo-growth-case": {
        "eyebrow": "Business analysis · from SEC filings",
        "title": "Where Vimeo's next dollar comes from",
        "sub": "An outside-in analysis from Vimeo's 10-K and 10-Q filings: what drives revenue, three growth bets, a business "
               "case for the best one and the experiment that would decide it.",
        "stats": [["120×", "what an Enterprise account pays against a Self-Serve one"], ["0.68%", "upgrades a year for the bet to break even"],
                  ["$2.2M", "net present value at the 1% plan"]],
        "chips": ["Python", "Excel model", "Interactive model", "A/B test design"],
    },
    "excel-twin": {
        "eyebrow": "Open-source Python library",
        "title": "Prove the spreadsheet matches the model",
        "sub": "excel-twin checks that a workbook's live formulas reproduce a Python model, recalculates it with LibreOffice "
               "in CI and keeps .xlsx files byte-stable.",
        "stats": [["5", "analysis repositories reconcile through it"], ["3,134", "figures checked between Python and Excel"],
                  ["34.25", "ROUND(34.245, 2) the way Excel computes it"]],
        "chips": ["Python 3.12+", "openpyxl", "LibreOffice", "Typed"],
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
