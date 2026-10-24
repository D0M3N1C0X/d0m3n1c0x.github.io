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
    "ai-act-hr-readiness-kit": {
        "eyebrow": "EU AI Act · Regulation (EU) 2024/1689 and 2026/1744",
        "title": "Which of HR's AI systems are high-risk, and what do they owe?",
        "sub": "Every AI system an HR function in four countries uses, classified under the AI Act: what each one owes "
               "and from when, and whom to tell under national labour law.",
        "stats": [["1 of 12", "AI systems to stop now: emotion recognition in interviews"],
                  ["7", "high-risk systems, with duties from 2 December 2027"],
                  ["4 countries", "rules on telling the workers, already in force"]],
        "chips": ["Python", "Excel register", "Worker information pack", "Sourced rules"],
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
    "where-pay-transparency-bites": {
        "eyebrow": "Research · Eurostat, 27 Member States",
        "title": "The published pay gap understates what employers will find",
        "sub": "Split across 17 sectors, the 2022 gender pay gap is wider inside sectors than in the headline in 22 of "
               "27 Member States, most of all where the headline looks small. In R and Quarto.",
        "stats": [["14.6%", "EU gap inside the same sector, against 12.2% published"], ["3.8% → 14.4%", "Italy: published, then inside sectors"],
                  ["22 of 27", "Member States where the headline flatters"]],
        "chips": ["R", "Quarto", "Eurostat", "Working paper"],
    },
    "hr-people-analytics": {
        "eyebrow": "People analytics · attrition, pay equity, HR service",
        "title": "Why people leave, and what it costs",
        "sub": "Three questions a People function has to answer with numbers, end to end on a 4,000-employee European "
               "organisation: data model, SQL warehouse, statistics, charts and a report for leadership.",
        "stats": [["3.53×", "odds of resigning when paid below 0.92 compa-ratio"], ["13.6%", "voluntary turnover, 16.8% in Customer Service"],
                  ["76.4%", "SLA attainment against a 90% target"]],
        "chips": ["Python, no dependencies", "SQL", "Statistics", "Report"],
    },
    "engagement-survey-analytics": {
        "eyebrow": "People analytics · employee engagement survey",
        "title": "From 2,753 answers to what to do on Monday",
        "sub": "An engagement survey analysed end to end: non-response bias, scores with confidence intervals, a key-driver "
               "analysis that survives a bootstrap, and free text that reports its own error rate.",
        "stats": [["40%", "of the explained variance carried by Manager Support"], ["−12", "eNPS, with an engagement index of 54%"],
                  ["34", "teams significantly below the company score"]],
        "chips": ["Python, no dependencies", "Statistics", "Text analytics", "Live dashboard"],
    },
    "job-search-agent": {
        "eyebrow": "Automation · a job search as a data pipeline",
        "title": "A job search that runs as a pipeline",
        "sub": "Postings from public ATS board APIs, scored against a profile with rules you can read, tailored documents, "
               "and funnel analytics on which positioning gets replies. Zero dependencies.",
        "stats": [["8", "ATS providers, fetching split from parsing"], ["325", "company boards in the catalogue"],
                  ["344", "offline tests"]],
        "chips": ["Python, no dependencies", "CLI", "Dashboard", "Funnel analytics"],
    },
    "pompei-stratificata": {
        "eyebrow": "Public history · Pompeii and Herculaneum, AD 79 to today",
        "title": "Pompeii never vanished: it became unreadable",
        "sub": "Two cities buried by the same night, in a model you walk through: eight phases from the eve of the eruption "
               "to today's excavation, the two stratigraphic columns side by side, and a dossier with a source for every statement.",
        "stats": [["8", "phases, from AD 79 to today's excavation"], ["5 m vs 20 m", "of deposit: Pompeii against Herculaneum"],
                  ["6", "languages, and it works offline"]],
        "chips": ["three.js", "Sourced dossier", "Six languages", "Installable app"],
    },
    "firenze-1216-citta": {
        "eyebrow": "Media education · Florence, Easter morning 1216",
        "title": "Walk the city of the Buondelmonte murder",
        "sub": "Florence inside its 1172–75 walls, house by house, on two days: the broken promise of 10 February and Easter "
               "morning. The explorable setting of a serious game for schools, still in development.",
        "stats": [["1216", "Easter morning, the day of the murder"], ["2", "days to walk through, at any hour"],
                  ["1172–75", "circle of walls, gates and suburbs, rebuilt"]],
        "chips": ["three.js", "Vite", "Game scenes", "Prototype"],
    },
    "spinwall": {
        "eyebrow": "Web app · iPhone, iPad and Mac",
        "title": "Your albums, on a Cover Flow wall",
        "sub": "Flip through the albums you have listened to, turn a cover over for its songs, and keep your own notes. "
               "Everything stays on the device: no account, no server.",
        "stats": [["0", "accounts or servers"], ["3", "devices from one web app"], ["2", "free catalogues: iTunes and Wikipedia"]],
        "chips": ["JavaScript", "IndexedDB", "Installable", "SwiftUI next"],
    },
    "d0m3n1c0x.github.io": {
        "eyebrow": "Portfolio · HR advisory, people analytics, reward",
        "title": "Domenico Perroni",
        "sub": "I build the analysis an HR function runs on: payroll checks, pay transparency reporting, workforce costs and "
               "business cases. Every figure computed twice or traced to its source.",
        "stats": [["3,502", "figures reconciled between Python and Excel"], ["12", "projects to open live, nothing to install"],
                  ["5", "languages: Italian, English, Spanish, French, Polish"]],
        "chips": ["Payroll", "Pay transparency", "Workforce planning", "Business analysis"],
    },
    "excel-twin": {
        "eyebrow": "Open-source Python library",
        "title": "Prove the spreadsheet matches the model",
        "sub": "excel-twin checks that a workbook's live formulas reproduce a Python model, recalculates it with LibreOffice "
               "in CI and keeps .xlsx files byte-stable.",
        "stats": [["6", "analysis repositories reconcile through it"], ["3,502", "figures checked between Python and Excel"],
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
