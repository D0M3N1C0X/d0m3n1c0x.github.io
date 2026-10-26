"""
One-page case studies, in the shape a consulting firm uses: the client's question, what was done, what it found,
what real data would change, and how the work is checked. Each case is a page on the site (cases/<slug>.html) and the
same page as an A4 PDF to attach to an application (cases/<slug>.pdf), printed in the light theme.

Every figure is copied from the project's README as published on AS_OF; when a project changes its headline
numbers, change them here too.

    .venv/bin/python tools/cases.py          # pages, index and PDFs
"""
import html
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cases"
SITE = "https://d0m3n1c0x.github.io"
REPO = "https://github.com/D0M3N1C0X"
AS_OF = "24 October 2026"

CASES = [
    {
        "slug": "pay-transparency-readiness",
        "repo": "pay-transparency-readiness-kit",
        "tag": "Reward & HR consulting",
        "title": "Is a four-country employer ready for the EU Pay Transparency Directive?",
        "client": "A synthetic employer with 3,443 workers in Italy, Poland, Germany and Spain, about to file its first "
                  "pay gap reports under Directive (EU) 2023/970.",
        "question": "When do we report, what will the numbers say, where are the gaps and why, and what would closing "
                    "them cost?",
        "did": [
            "Computed the seven Article 9 reporting items and the Article 10 screen for every employer and category of "
            "workers, on hourly and on annual pay.",
            "Built the categories of equal value with a gender-neutral job evaluation, and tested its weights against "
            "the EU guidelines published by the Commission and EIGE in March 2026.",
            "Read the Italian decree in the Gazzetta Ufficiale and reported Milan on both measures: the Directive's "
            "total pay and Italy's fixed pay (livello retributivo).",
            "Delivered a live Excel model, a board briefing, a readiness checklist and a browser tool that runs the same "
            "assessment on a client's payroll without the file leaving the computer.",
        ],
        "kpis": [("17.6%", "hourly gender pay gap across the group"),
                 ("12 of 28", "categories of workers to justify or remedy by 7 Dec 2027"),
                 ("≤ €1.9M", "a year to close every flagged gap"),
                 ("1 of 14", "obligations already in place")],
        "found": [
            "Bonus, commission and allowances add 2.2 points to a 15.4% base-pay gap. In Sales, commission is 12.6% of "
            "base pay for women and 15.1% for men under identical rules: territories are allocated unequally.",
            "In Italy the decree counts fixed pay only: Milan's gap is 18.0% on that measure against 19.7% on total pay, "
            "and what each flagged category has to justify changes.",
        ],
        "real": [
            "Calendar-year payroll instead of a snapshot, with leavers and pay after leave.",
            "In Italy, the collective agreement's levels as the starting categories (D.lgs. 96/2026, art. 4).",
            "A justification workshop per flagged category, before the cost is budgeted.",
        ],
        "checked": "511 figures reconciled between the Excel formulas and pandas; the browser tool checked on 4,452 "
                   "values; every legal statement in a verification register with its source.",
        "links": [("Read the report", f"{SITE}/pay-transparency-readiness-kit/"),
                  ("Try the tool", f"{SITE}/pay-transparency-readiness-kit/tool/")],
        "skills": ["Directive (EU) 2023/970", "Job evaluation", "Excel modelling", "Python", "Board communication"],
    },
    {
        "slug": "ai-act-hr-readiness",
        "repo": "ai-act-hr-readiness-kit",
        "tag": "AI governance · HR",
        "title": "Which of HR's AI systems are high-risk, and what do they owe?",
        "client": "The same four-country employer, whose HR function uses twelve AI systems, from CV screening to a "
                  "pay review recommender and an attrition model built in-house.",
        "question": "Which systems does the AI Act ban or class as high-risk, what does each owe and from when, and whom "
                    "do we have to tell before we use them?",
        "did": [
            "Read the AI Act and the Digital Omnibus (Regulation (EU) 2026/1744) in the Official Journal.",
            "Classified each system from eighteen answers: prohibited, high-risk, not high-risk under Article 6(3), "
            "transparency only or minimal, with the reason written next to it, and when its duties bite under the "
            "amended Article 111(2).",
            "Mapped thirteen obligations, and the national rules on informing workers in four countries.",
            "Delivered a live Excel register, a report, model notices per country and a browser tool.",
        ],
        "kpis": [("1 of 12", "systems to stop now: emotion recognition in interviews"),
                 ("7", "high-risk systems, with duties from 2 December 2027"),
                 ("1", "system built in-house that makes the employer a provider"),
                 ("11 · 5+", "systems to tell the German works council about · that need its agreement")],
        "found": [
            "A video interview pilot infers candidates' emotions: prohibited since February 2025.",
            "National labour law binds before the AI Act does: Spain owes the works council the parameters of seven "
            "systems; Italy requires a written notice for the fully automated shift rota.",
            "Already on the market is not a free pass: the seven high-risk systems fall under the duties at their next "
            "significant design change (Art. 111(2)), and cloud HR software changes often.",
        ],
        "real": [
            "The suppliers' instructions for use and their Article 6(4) assessments, on file.",
            "The Commission's guidelines on high-risk classification applied to the boundary cases.",
            "A labour lawyer in each country to confirm the notices before they go out.",
        ],
        "checked": "330 figures reconciled between the Excel formulas and Python, recalculated by LibreOffice on every "
                   "change; the browser tool checked against Python on 12,090 values; an independent legal and code "
                   "review on 24 October 2026, its fixes in v1.1.0.",
        "links": [("Try the tool", f"{SITE}/ai-act-hr-readiness-kit/tool/"),
                  ("Read the report", f"{SITE}/ai-act-hr-readiness-kit/")],
        "skills": ["EU AI Act", "Labour law IT/DE/ES/PL", "AI governance", "Excel modelling", "Python"],
    },
    {
        "slug": "equal-value-pay-ranges",
        "repo": "equal-value-pay-ranges",
        "tag": "Reward",
        "title": "From family pay bands to one range per grade and country",
        "client": "The same four-country employer, paying through bands built family by family, with one head-office "
                  "scale cut down by a fixed share for each country.",
        "question": "Our bands pay the family, not the job. What should equal-value ranges look like, what will the move "
                    "cost, and what do we publish in job ads?",
        "did": [
            "Measured how far the current bands pay the family rather than the grade of equal value.",
            "Priced one range per grade and country on Eurostat market data for the same occupations.",
            "Placed every employee against the new range, costing who falls below the minimum and who sits above "
            "the maximum.",
            "Built a range finder that gives recruiters the range to publish for any vacancy (Article 5).",
        ],
        "kpis": [("39%", "Tech's midpoint above Customer Service's at the same level"),
                 ("−9.7% to +13.6%", "payroll against the market, Germany to Poland"),
                 ("€3.02M", "a year to bring 824 people to the new minimum, 58% of it for women"),
                 ("€3.48M", "a year of pay protected for 739 people above the maximum")],
        "found": [
            "Inside one grade of equal value, midpoints differ by up to 74%.",
            "The bands put Poland at 81% of Italy; the market puts it at 66%. In Italy 42% of women fall below the new "
            "minimum against 26% of men.",
        ],
        "real": [
            "A salary survey (Mercer, WTW, Korn Ferry) in place of Eurostat's averages.",
            "The job evaluation agreed with workers' representatives before the ranges are set.",
            "A phased plan, with the protected pay brought into range over two or three reviews.",
        ],
        "checked": "1,315 figures reconciled between the Excel formulas and pandas, recalculated by LibreOffice on every "
                   "change; every market figure traced to its Eurostat table.",
        "links": [("Read the report", f"{SITE}/equal-value-pay-ranges/"),
                  ("Try the range finder", f"{SITE}/equal-value-pay-ranges/ads.html")],
        "skills": ["Pay structures", "Market pricing", "Compa-ratio", "Excel modelling", "Python"],
    },
    {
        "slug": "workforce-cost-model",
        "repo": "workforce-cost-model",
        "tag": "HR & finance",
        "title": "What will next year's people cost be?",
        "client": "An employer in Milan and Kraków closing its FY2026 people budget and planning FY2027.",
        "question": "What does one person really cost in each country, why did last year overrun, and what does next "
                    "year cost if we freeze hiring, lose more people or start closing pay gaps?",
        "did": [
            "Loaded every employee with each employer contribution, cap by cap: INPS and TFR in Italy; ZUS, the Labour "
            "Fund, FGŚP and PPK in Poland.",
            "Split the FY2026 variance into volume, mix and rate, adding up exactly to the overrun.",
            "Forecast FY2027 month by month under four scenarios, moving FTE rather than people.",
            "Built a simulator for the budget meeting, with the cost of one employee in four countries.",
        ],
        "kpis": [("€5.8M", "over the FY2026 budget (5.7%), explained by volume"),
                 ("€59,382", "a fully loaded FTE in Milan, against €41,727 in Kraków"),
                 ("€111.0M", "FY2027 in the base case (+3.6%)"),
                 ("€0.76M", "added in FY2027 by closing pay gaps from January")],
        "found": [
            "A hiring freeze from October cuts FY2027 to €104.6M but ends the year with 278 fewer FTE: a capacity "
            "decision, not a finance one.",
            "Higher attrition barely moves payroll but lifts recruitment cost to €1.54M.",
        ],
        "real": [
            "Actual payroll by month, with the company's own on-cost rules and benefits.",
            "Hiring and leaver plans by team from the business, not last year's rates.",
            "The pay-gap remediation from the client's own Article 10 screen.",
        ],
        "checked": "570 figures reconciled between the Excel formulas and pandas; the simulator checked against the model "
                   "on 9,679 values; every rate and cap in a register with its source.",
        "links": [("Read the CFO memo", f"{SITE}/workforce-cost-model/"),
                  ("Try the simulator", f"{SITE}/workforce-cost-model/simulator/")],
        "skills": ["Workforce planning", "Budget variance", "Employer costs IT/PL/DE/ES", "Excel modelling", "Python"],
    },
    {
        "slug": "controlli-cedolini",
        "repo": "controlli-cedolini",
        "tag": "Payroll operations",
        "title": "Catching payroll errors before the client does",
        "client": "An Italian payroll provider sending payslips for three clients and 122 employees under the CCNL "
                  "Terziario, with errors planted on purpose.",
        "question": "Which payslips are wrong before they go out, by how much, and what does the November 2026 pay "
                    "increase cost each client?",
        "did": [
            "Wrote fourteen checks that recompute each item from the collective agreement's rules, not from the payroll "
            "software: minimums, seniority steps, INPS, TFR, holidays, 13th and 14th month, leavers, notice.",
            "Reconciled the F24 tax payment with the sum of each client's payslips.",
            "Delivered the checks three ways that agree: Python, a live-formula sheet for Google Sheets and a browser "
            "tool in English and Italian.",
        ],
        "kpis": [("35 of 35", "planted errors found, with no false alarms"),
                 ("6", "employees below the minimum: €175.44 a month plus arrears"),
                 ("€212.40", "less withholding tax in one F24 than the payslips add up to"),
                 ("€2,379.98", "a month to pay in November 2026, after absorption")],
        "found": [
            "Three of six leavers carry an error: the 14th month counted from January, untaken holiday paid at 1/30, a "
            "dismissal with half the notice the agreement requires.",
            "Each flag comes with the expected value, the value found and what to do.",
        ],
        "real": [
            "A pilot on one client's real payslips, run in the browser so the files never leave the office.",
            "The other collective agreements the provider's clients apply.",
            "A monthly record of what the checks caught, to measure the errors avoided.",
        ],
        "checked": "The sheet checked against Python on 580 values; the browser tool on 2,219 values, half-cent "
                   "alterations and Italian file formats included; every rule with its source in the agreement.",
        "links": [("Try the tool", f"{SITE}/controlli-cedolini/strumento/?lang=en"),
                  ("Read the report (Italian)", f"{SITE}/controlli-cedolini/")],
        "skills": ["Italian payroll", "CCNL Terziario", "Process controls", "Google Sheets", "Python"],
    },
    {
        "slug": "vimeo-growth-case",
        "repo": "vimeo-growth-case",
        "tag": "Business analysis",
        "title": "Where will Vimeo's next dollar come from?",
        "client": "Vimeo at the handover to Bending Spoons (November 2025), read from the outside through its SEC "
                  "filings from 2021 to Q3 2025.",
        "question": "What drives revenue today, where could growth come from, and which bet is worth testing before "
                    "anyone is hired for it?",
        "did": [
            "Split revenue into volume and price by category, each figure traced to its filing.",
            "Sized three growth bets and built the business case for routing Self-Serve accounts to Enterprise.",
            "Designed the A/B test that would decide it, with sample sizes and a decision rule measured on simulated "
            "tests.",
        ],
        "kpis": [("−21%", "Self-Serve subscribers 2021-2024, while ARPU rose 9%"),
                 ("$23.2M → $83.2M", "Enterprise revenue in three years; bookings −2% in Q3 2025"),
                 ("0.68%", "upgrades a year per eligible account to break even"),
                 ("$2.2M", "net present value at the 1% plan")],
        "found": [
            "An Enterprise account pays about 120 times a Self-Serve one, and the filings say Enterprise is often an "
            "upgrade from Self-Serve: the lever sits between the two.",
            "A 180-day one-sided test on 20,982 of the 22,558 eligible accounts can tell.",
        ],
        "real": [
            "Account-level upgrade history instead of the filings' aggregates.",
            "The sales team's real capacity and the first Enterprise deal size by segment.",
            "The test run, and the decision rule applied as written.",
        ],
        "checked": "The Excel model checked against Python on 209 values; the interactive model's JavaScript on 1,200 "
                   "values from 40 random scenarios, sample sizes included.",
        "links": [("Read the memo", f"{SITE}/vimeo-growth-case/"),
                  ("Move the assumptions", f"{SITE}/vimeo-growth-case/model/")],
        "skills": ["SEC filings", "Business case", "Experiment design", "Excel modelling", "Python"],
    },
    {
        "slug": "where-pay-transparency-bites",
        "repo": "where-pay-transparency-bites",
        "tag": "Research",
        "title": "Why the published gender pay gap flatters",
        "client": "Any HR or reward team about to benchmark its first pay gap report against the national figure "
                  "Eurostat publishes.",
        "question": "Is the national gap the right benchmark, and where will pay transparency bite hardest?",
        "did": [
            "Decomposed the published 2022 gap of each of the 27 Member States into a between-sector and a "
            "within-sector part, reconciled with Eurostat's own figures.",
            "Set each country's within-sector gap against its exposure to annual reporting: the share of employees in "
            "enterprises of 250 or more.",
            "Published an article, a working paper and an explorer for every country, all rebuilt from data snapshots "
            "in R and Quarto.",
        ],
        "kpis": [("12.2% → 14.6%", "EU gap, published against within sectors, 2022"),
                 ("22 of 27", "Member States where the gap inside sectors is wider"),
                 ("3.8% → 14.4%", "Italy, published against within sectors"),
                 ("51%", "of employees in enterprises that report every year")],
        "found": [
            "Women are over-represented in sectors that pay above average, such as education and health, which lowers "
            "the national figure: the lowest headlines hide the most.",
            "In all six countries with complete data by enterprise size, the gap is wider in the enterprises of 250 or "
            "more, the first to report.",
        ],
        "real": [
            "A client's own report set against its sector's within-sector gap, not the national one.",
            "The 2026 Structure of Earnings Survey when Eurostat releases it.",
        ],
        "checked": "Decomposition identities and the reconciliation with Eurostat's published gaps tested in R (64 "
                   "tests); every table rebuilt from pinned snapshots.",
        "links": [("Read the article", f"{SITE}/where-pay-transparency-bites/"),
                  ("Open the explorer", f"{SITE}/where-pay-transparency-bites/dashboard/")],
        "skills": ["Eurostat SES", "Decomposition", "R and Quarto", "Research writing", "Data visualisation"],
    },
]

CSS = """
:root{--paper:#ffffff;--paper-2:#f5f5f7;--surface:#ffffff;--ink:#1d1d1f;--ink-soft:#424245;--muted:#6e6e73;
--line:#e8e8ed;--accent:#0066cc;--accent-wash:#eef5fd;--glow:none;
--font:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
--display:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#000000;--paper-2:#0b0c0f;--surface:#15171c;
--ink:#f5f5f7;--ink-soft:#c7c9d1;--muted:#8b8f9a;--line:#23262e;--accent:#4f8cff;--accent-wash:#101b33;color-scheme:dark;
--glow:radial-gradient(55% 70% at 90% 0%,rgba(79,140,255,.22),transparent 70%)}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);background-image:var(--glow);background-repeat:no-repeat;color:var(--ink);
font:400 15px/1.5 var(--font);-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}
.page{max-width:820px;margin:0 auto;padding:40px 24px 56px}
.top{display:flex;justify-content:space-between;gap:16px;font-size:13px;color:var(--muted)}
.top a{color:var(--muted)}
.tag{display:inline-block;margin-top:28px;padding:4px 12px;border-radius:999px;background:var(--accent-wash);
color:var(--accent);font-size:12px;font-weight:600;letter-spacing:.02em;text-transform:uppercase}
h1{font:700 34px/1.12 var(--display);letter-spacing:-.02em;margin:12px 0 10px}
.client{color:var(--ink-soft);margin:0 0 18px;font-size:15px}
.q{border-left:3px solid var(--accent);padding:2px 0 2px 14px;margin:0 0 22px;font-size:17px;font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:0 0 22px}
.kpi{background:var(--paper-2);border:1px solid var(--line);border-radius:14px;padding:12px 12px 10px}
.kpi b{display:block;font:700 21px/1.15 var(--display);letter-spacing:-.01em;margin-bottom:4px}
.kpi span{display:block;font-size:12px;line-height:1.35;color:var(--ink-soft)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:26px}
h2{font:650 13px/1.3 var(--font);letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin:0 0 8px}
ul{margin:0 0 18px;padding-left:18px}li{margin:0 0 6px}
.check{background:var(--paper-2);border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:4px 0 18px;font-size:14px}
.skills{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 18px}
.skills span{border:1px solid var(--line);border-radius:999px;padding:3px 10px;font-size:12.5px;color:var(--ink-soft)}
.links{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:14px;font-weight:600}
.foot{margin-top:22px;padding-top:12px;border-top:1px solid var(--line);font-size:12px;color:var(--muted)}
.list{display:grid;gap:12px;margin-top:24px}
.item{display:block;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--line);
border-radius:16px;padding:16px 18px}
.item:hover{border-color:var(--accent)}
.item small{color:var(--accent);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.03em}
.item strong{display:block;font:650 19px/1.25 var(--display);margin:4px 0}
.item span{color:var(--ink-soft);font-size:14px}
@media (max-width:680px){.kpis{grid-template-columns:1fr 1fr}.cols{grid-template-columns:1fr;gap:0}h1{font-size:28px}}
@page{size:A4;margin:12mm 13mm}
@media print{:root{--paper:#fff;--paper-2:#f5f5f7;--ink:#1d1d1f;--ink-soft:#424245;--muted:#6e6e73;--line:#e8e8ed;
--accent:#0066cc;--accent-wash:#eef5fd;--glow:none}body{font-size:12.4px}.page{padding:0;max-width:none}
.top .web{display:none}h1{font-size:26px;margin-top:8px}.tag{margin-top:12px}.q{font-size:14.5px;margin-bottom:14px}
.client{font-size:12.6px;margin-bottom:12px}.kpis{margin-bottom:14px}.kpi b{font-size:17px}.kpi span{font-size:10.5px}
li{margin-bottom:4px}ul{margin-bottom:12px}.check{font-size:11.6px;margin-bottom:12px}.links a::after{content:" " attr(href);
font-weight:400;color:#6e6e73}}
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def page(c: dict) -> str:
    ul = lambda items: "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>"
    kpis = "".join(f'<div class="kpi"><b>{esc(v)}</b><span>{esc(t)}</span></div>' for v, t in c["kpis"])
    links = "".join(f'<a href="{esc(u)}">{esc(t)}</a>' for t, u in
                    [*c["links"], ("The repository", f"{REPO}/{c['repo']}")])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(c['title'])} · Case study</title>
<meta name="description" content="{esc(c['question'])}">
<style>{CSS}</style></head>
<body><main class="page">
<div class="top"><span>Case study · Domenico Perroni</span>
<span class="web"><a href="./">All case studies</a> · <a href="{c['slug']}.pdf">PDF</a></span></div>
<span class="tag">{esc(c['tag'])}</span>
<h1>{esc(c['title'])}</h1>
<p class="client"><b>Client:</b> {esc(c['client'])}</p>
<p class="q">{esc(c['question'])}</p>
<div class="kpis">{kpis}</div>
<div class="cols">
<section><h2>What I did</h2>{ul(c['did'])}</section>
<section><h2>What it found</h2>{ul(c['found'])}<h2>With real data</h2>{ul(c['real'])}</section>
</div>
<p class="check"><b>How it is checked.</b> {esc(c['checked'])}</p>
<div class="skills">{"".join(f"<span>{esc(s)}</span>" for s in c['skills'])}</div>
<div class="links">{links}</div>
<p class="foot">Synthetic or public data; not legal, pay or investment advice. Figures as published on
{AS_OF}. Domenico Perroni · HR advisory, people analytics, reward · Kraków ·
<a href="{SITE}/">d0m3n1c0x.github.io</a></p>
</main></body></html>
"""


def index() -> str:
    items = "".join(f'<a class="item" href="{c["slug"]}.html"><small>{esc(c["tag"])}</small>'
                    f'<strong>{esc(c["title"])}</strong><span>{esc(c["question"])}</span></a>' for c in CASES)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Case studies · Domenico Perroni</title>
<meta name="description" content="Seven one-page case studies: the question, what was done, what it found.">
<meta property="og:type" content="website">
<meta property="og:title" content="Case studies · Domenico Perroni">
<meta property="og:description" content="Seven client questions, one page each: what was done, what it found and what real data would change.">
<meta property="og:url" content="https://d0m3n1c0x.github.io/cases/">
<meta property="og:image" content="https://d0m3n1c0x.github.io/media/og-cases.png">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="640">
<meta property="og:image:alt" content="Seven client questions, one page each; 3,515 values reconciled between Excel and Python.">
<meta name="twitter:card" content="summary_large_image">
<style>{CSS}</style></head>
<body><main class="page">
<div class="top"><span>Domenico Perroni</span><span class="web"><a href="../">Portfolio</a></span></div>
<h1 style="margin-top:28px">Case studies</h1>
<p class="client">One page each, in the shape a consulting firm uses: the client's question, what was done, what it
found, and what real data would change. Every page is also a PDF to attach to an application.</p>
<div class="list">{items}</div>
</main></body></html>
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(index(), encoding="utf-8")
    changed = []
    for c in CASES:
        html_path, pdf = OUT / f"{c['slug']}.html", OUT / f"{c['slug']}.pdf"
        text = page(c)
        if not pdf.exists() or not html_path.exists() or html_path.read_text(encoding="utf-8") != text:
            changed.append(c)
        html_path.write_text(text, encoding="utf-8")
    # PDFs only for pages that changed: Chrome stamps every PDF with a new date, so an unchanged case keeps its bytes
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        pg = browser.new_page()
        for c in changed:
            pg.goto((OUT / f"{c['slug']}.html").as_uri())
            pg.emulate_media(media="print", color_scheme="light")
            pg.pdf(path=str(OUT / f"{c['slug']}.pdf"), format="A4", print_background=True,
                   margin={"top": "12mm", "bottom": "12mm", "left": "13mm", "right": "13mm"})
            print(f"{c['slug']}: html + pdf")
        browser.close()


if __name__ == "__main__":
    main()
