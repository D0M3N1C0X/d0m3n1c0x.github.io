"""
One-page case studies, in the shape a consulting firm uses: the client's question, what was done, what it found,
what real data would change, and how the work is checked. Each case is a page on the site (cases/<slug>.html) and the
same page as an A4 PDF to attach to an application (cases/<slug>.pdf), printed in the light theme.

Every figure is copied from the project's README as published on AS_OF, or on the case's own "as_of" when it was
updated later; when a project changes its headline numbers, change them here too, with the date.

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
        "as_of": "8 November 2026",
        "client": "The same four-country employer, whose HR function uses twelve AI systems, from CV screening to a "
                  "pay review recommender and an attrition model built in-house.",
        "question": "Which systems does the AI Act ban or class as high-risk, what does each owe and from when, and whom "
                    "do we have to tell before we use them?",
        "did": [
            "Read the AI Act and the Digital Omnibus (Regulation (EU) 2026/1744) in the Official Journal.",
            "Classified each system from eighteen answers: prohibited, high-risk, not high-risk under Article 6(3), "
            "transparency only or minimal, with the reason written next to it, and when its duties bite under the "
            "amended Article 111(2).",
            "Mapped fifteen obligations, including the fundamental rights impact assessment and registration that "
            "public bodies owe, and the national rules on informing workers in nine countries.",
            "Wrote what to ask each supplier (sixteen questions, each tied to a duty), an AI literacy plan for named "
            "groups, and a draft impact assessment per high-risk system that reuses the DPIA.",
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
        "checked": "813 figures reconciled between the Excel formulas and Python, recalculated by LibreOffice on every "
                   "change; the browser tool checked against Python on 16,309 values; every legal statement read in "
                   "the official text and logged with its source.",
        "links": [("Try the tool", f"{SITE}/ai-act-hr-readiness-kit/tool/"),
                  ("Read the report", f"{SITE}/ai-act-hr-readiness-kit/")],
        "skills": ["EU AI Act", "Labour law in nine countries", "AI governance", "Excel modelling", "Python"],
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
        "as_of": "8 November 2026",
        "client": "An employer in Milan, Kraków, Munich and Barcelona, four months into FY2027.",
        "question": "What does one person really cost in each country, why did last year overrun, what does next year "
                    "cost under each scenario, and where is it heading now that four months have closed?",
        "did": [
            "Loaded every employee with each employer contribution, ceiling by ceiling: INPS and TFR in Italy; ZUS, "
            "PPK and the funds in Poland; German social insurance; Spanish Seguridad Social and its solidarity "
            "contribution.",
            "Split the FY2026 variance into volume, mix and rate, adding up exactly to the overrun.",
            "Forecast FY2027 month by month under five scenarios, renewals and the zloty included; then re-forecast "
            "it from the closed months and turned a June 2027 headcount target into hires a month.",
            "Built a simulator for the budget meeting, with the cost of one employee in four countries.",
        ],
        "kpis": [("€9.9M", "over the FY2026 budget (5.6%), explained by volume"),
                 ("€74,887", "a fully loaded FTE in Munich, against €41,727 in Kraków"),
                 ("€192.9M", "FY2027 in the base case (+4.0%)"),
                 ("64 a month", "hires from January to land on the June 2027 plan")],
        "found": [
            "After October the year is €0.18M over budget for the wrong reasons: fewer people save €0.60M, a higher "
            "cost per FTE, mostly in Kraków, adds €0.77M.",
            "A hiring freeze from October cuts FY2027 to €182.6M but ends the year with 411 fewer FTE: a capacity "
            "decision, not a finance one.",
            "Collective renewals and a stronger zloty would add €4.45M, €3.12M of it from the exchange rate alone.",
        ],
        "real": [
            "Actual payroll by month, with the company's own on-cost rules and benefits.",
            "Hiring and leaver plans by team from the business, not last year's rates.",
            "The pay-gap remediation from the client's own Article 10 screen.",
        ],
        "checked": "1,649 figures reconciled between the Excel formulas and pandas; the simulator checked against the "
                   "model on 43,152 values; every rate and ceiling in a register with its source; the closed months "
                   "of FY2027 are synthetic and say so.",
        "links": [("Read the CFO memo", f"{SITE}/workforce-cost-model/"),
                  ("Try the simulator", f"{SITE}/workforce-cost-model/simulator/")],
        "skills": ["Workforce planning", "Budget variance", "Employer costs IT/PL/DE/ES", "Excel modelling", "Python"],
    },
    {
        "slug": "controlli-cedolini",
        "repo": "controlli-cedolini",
        "tag": "Payroll operations",
        "title": "Catching payroll errors before the client does",
        "as_of": "9 November 2026",
        "client": "An Italian payroll provider sending payslips for six clients and 182 employees under four collective "
                  "agreements (retail and services, engineering industry, bars and restaurants, logistics), with errors "
                  "planted on purpose.",
        "question": "Which payslips are wrong before they go out, by how much, and what does the November 2026 pay "
                    "increase cost each client?",
        "did": [
            "Wrote twenty-two checks that recompute each item from the client's agreement, INPS and the 2026 tax law, "
            "not from the payroll software: minimums, INPS rates, sick and maternity pay, income tax, TFR, notice.",
            "Read each agreement's rules in the texts its signatories publish or filed at CNEL, and kept them in one "
            "table: steps, monthly payments, part months, holidays, notice, sick pay and top-up.",
            "Reconciled the F24 tax payment with the sum of each client's payslips.",
            "Delivered the checks three ways that agree: Python, a live-formula sheet for Google Sheets and a browser "
            "tool in English and Italian.",
        ],
        "kpis": [("67 of 67", "planted errors found, with no false alarms"),
                 ("10", "employees below their agreement's minimum: €305.24 a month plus arrears"),
                 ("€212.40", "less withholding tax in one F24 than the payslips add up to"),
                 ("€2,448.98", "a month to pay in November 2026, after absorption")],
        "found": [
            "Five contributions withheld at the wrong rate: CIGS and the FIS share missing above 15 staff on average, "
            "CIGS taken below it, the extra 1% forgotten above €4,685 a month.",
            "Leavers carry errors in the 14th month, holiday, notice and severance: a coefficient from the wrong month, "
            "the 17% substitute tax not deducted.",
            "Most errors in the new clients are another agreement's rule applied by mistake: steps every three years "
            "where they are every two, 50% sick pay where bars and restaurants get 80%.",
        ],
        "real": [
            "A pilot on one client's real payslips, run in the browser so the files never leave the office.",
            "Blue-collar staff and drivers, whose sick pay base and notice follow other rules.",
            "A monthly record of what the checks caught, to measure the errors avoided.",
        ],
        "checked": "The sheet checked against Python on 1,682 values; the browser tool on 3,909 values, half-cent "
                   "alterations and Italian file formats included; every rule with its source in the agreement, an "
                   "INPS circular or ISTAT's indices.",
        "links": [("Try the tool", f"{SITE}/controlli-cedolini/strumento/?lang=en"),
                  ("Read the report (Italian)", f"{SITE}/controlli-cedolini/")],
        "skills": ["Italian payroll", "Four CCNLs", "Process controls", "Google Sheets", "Python"],
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
    {
        "slug": "hr-people-analytics",
        "repo": "hr-people-analytics",
        "translation": "hr-people-analytics-it",
        "media": ("hpa-tool", "The retention check on the example file: turnover by department, how long people stay, "
                              "what goes with resigning, warning signs per team."),
        "tag": "People analytics",
        "title": "Who leaves, and may a model say who?",
        "as_of": "24 November 2026",
        "client": "A shared-services organisation of 4,000 employees in Italy, Poland, Germany and Spain (synthetic), "
                  "whose HR team wants a retention model and has to decide whether it may use one.",
        "question": "Who leaves and when, can a model warn in time, is it fair, and what may HR do with it under the "
                    "AI Act?",
        "did": [
            "Fitted an attrition model on one quarter and scored it on the next two, which it had never seen, against a "
            "checklist of the same signs and the data's own ceiling.",
            "Audited it by sex, age, country and working time, and wrote its model card: the provider's answers to the "
            "14 questions the AI Act register asks of a high-risk system.",
            "Measured how long people stay with survival analysis on tenure, counting people hired before the data "
            "began from the tenure they had then.",
            "Delivered a browser tool for the client's own HRIS export, teams never names, and a workbook reconciled "
            "with Python.",
        ],
        "kpis": [("0.75", "AUC on quarters the model never saw; counting the same signs gets 0.72"),
                 ("38%", "of next quarter's resignations in the top 10% of scores"),
                 ("77 of 100", "hires still here after a year; 94 if early leavers are miscounted"),
                 ("88%", "of flagged people stay: why the card rules out decisions")],
        "found": [
            "Most of the value is in knowing which signs to watch: the weights add 0.03 of AUC over counting them, and "
            "the model closes 84% of the gap between chance and the ceiling.",
            "Country of work is not an input, so Germany is over-read, 3.6% predicted where 2.2% resign. Fixing it is a "
            "significant change under the AI Act, so the provider's duties come first.",
            "People paid below band stay 22.4 of their first 36 months against 31.3, the same effect in year one as "
            "after it.",
        ],
        "real": [
            "Inputs as they stood on each scoring date, with pay position changing at every raise.",
            "A decision on the engagement input: an individual survey score breaks the confidentiality most surveys "
            "promise.",
        ],
        "checked": "Statistics written from scratch and tested against closed forms (AUC as Mann-Whitney, the Cox "
                   "score test as the log-rank test); the tool agrees with Python on 1,530 values, the workbook on "
                   "121, recalculated by LibreOffice in CI.",
        "links": [("Read the report", f"{SITE}/hr-people-analytics/"),
                  ("Try the tool", f"{SITE}/hr-people-analytics/tool/"),
                  ("Model card", f"{REPO}/hr-people-analytics/blob/main/docs/model_card.md")],
        "skills": ["People analytics", "Model validation", "Survival analysis", "EU AI Act", "Python, no dependencies"],
    },
    {
        "slug": "hr-people-analytics-it",
        "repo": "hr-people-analytics",
        "lang": "it",
        "translation": "hr-people-analytics",
        "media": ("hpa-tool", "Lo strumento sul file d'esempio: turnover per reparto, quanto restano le persone, cosa si "
                              "accompagna alle dimissioni, segnali per reparto."),
        "tag": "People analytics",
        "title": "Chi se ne va, e può dirlo un modello?",
        "as_of": "24 novembre 2026",
        "client": "Un centro servizi condivisi di 4.000 dipendenti in Italia, Polonia, Germania e Spagna (dati "
                  "sintetici), il cui HR vuole un modello di retention e deve decidere se può usarlo.",
        "question": "Chi se ne va e quando, un modello può avvisare in tempo, è equo, e cosa può farne l'HR secondo "
                    "l'AI Act?",
        "did": [
            "Ho stimato un modello di attrition su un trimestre e l'ho applicato ai due successivi, mai visti, contro "
            "una checklist degli stessi segnali e il massimo raggiungibile sui dati.",
            "L'ho verificato per sesso, età, paese e orario, e ho scritto la sua scheda: le risposte del fornitore alle "
            "14 domande che il registro AI Act pone a un sistema ad alto rischio.",
            "Ho misurato quanto restano le persone con l'analisi di sopravvivenza sull'anzianità, contando chi era già "
            "assunto dall'anzianità che aveva quando iniziano i dati.",
            "Ho consegnato uno strumento nel browser per l'export del gestionale HR, per reparto e mai per nome, e un "
            "file Excel riconciliato con Python.",
        ],
        "kpis": [("0,75", "AUC su trimestri mai visti dal modello; contare gli stessi segnali dà 0,72"),
                 ("38%", "delle dimissioni del trimestre dopo nel 10% di punteggi più alti"),
                 ("77 su 100", "assunti ancora qui dopo un anno; 94 contando male chi se n'è andato prima"),
                 ("88%", "dei segnalati resta: per questo la scheda esclude le decisioni")],
        "found": [
            "Quasi tutto il valore sta nel sapere quali segnali guardare: i pesi aggiungono 0,03 di AUC rispetto a "
            "contarli, e il modello copre l'84% della distanza tra il caso e il massimo.",
            "Il paese di lavoro non è tra gli ingressi, così la Germania è sovrastimata, 3,6% previsto dove si dimette "
            "il 2,2%. Correggerlo è una modifica sostanziale per l'AI Act: prima vengono gli obblighi del fornitore.",
            "Chi è pagato sotto la fascia resta 22,4 dei primi 36 mesi contro 31,3, con lo stesso effetto nel primo "
            "anno e dopo.",
        ],
        "real": [
            "Ingressi presi com'erano a ogni data di calcolo, con la posizione in fascia che cambia a ogni aumento.",
            "Una decisione sull'engagement: il punteggio individuale del sondaggio rompe la riservatezza che quasi "
            "ogni sondaggio promette.",
        ],
        "checked": "Statistica scritta da zero e verificata su risultati noti (AUC come Mann-Whitney, il test score "
                   "di Cox come log-rank); lo strumento coincide con Python su 1.530 valori, l'Excel su 121, "
                   "ricalcolato da LibreOffice nella CI.",
        "links": [("Leggi il rapporto (inglese)", f"{SITE}/hr-people-analytics/"),
                  ("Prova lo strumento", f"{SITE}/hr-people-analytics/tool/?lang=it"),
                  ("Scheda del modello (inglese)", f"{REPO}/hr-people-analytics/blob/main/docs/model_card.md")],
        "skills": ["People analytics", "Validazione di modelli", "Analisi di sopravvivenza", "AI Act",
                   "Python senza dipendenze"],
    },
    {
        "slug": "job-search-agent",
        "repo": "job-search-agent",
        "translation": "job-search-agent-it",
        "media": ("jsa", "The dashboard: the roles worth an hour, why one scored 94, every posting with its verdict, "
                         "and the funnel."),
        "tag": "Automation · Recruitment",
        "title": "Which postings deserve an application?",
        "as_of": "15 November 2026",
        "client": "A job seeker in HR applying across Europe, with more postings than evenings. The figures are "
                  "measured on an invented candidate, so they can be published.",
        "question": "Which of this week's postings deserve an application, and how far can a scorer that decides it be "
                    "trusted?",
        "did": [
            "Pulled postings from the public APIs of eight applicant tracking systems and two job feeds, each source "
            "tested offline on a captured answer.",
            "Scored every posting against each positioning track with rules a person can read: hard gates first (a "
            "language actually required, years asked, location, seniority, terms), then keywords, every point explained.",
            "Wrote 160 postings labelled apply, maybe or skip for the candidate, and kept 30 aside, written after the "
            "last change to the rules, to measure each version on postings it was not tuned on.",
            "Delivered a dashboard, a CV and cover letter that may only cite the profile, and a one-line install.",
        ],
        "kpis": [("21 of 30", "held-out postings scored as labelled, up from 15 with the first rules"),
                 ("0 of 12", "postings worth applying to thrown away; all kept at least for review"),
                 ("15 of 15", "postings worth sending matched to the right positioning"),
                 ("306", "company boards, through 8 ATS APIs and 2 job feeds")],
        "found": [
            "The first rules scored half the held-out postings as a person would: 15 of 30. Rules written against "
            "labelled postings raised that to 20.",
            "The next version fixed every miss of its round and still scored 21 of 30 on a new held-out set, like "
            "the one before: phrase-by-phrase rules had stopped generalising. The report says so, and quotes that "
            "figure, not the 115 of 130 on the postings it was tuned on.",
            "The errors left are the cheap kind: three skips scored as worth applying, nothing worth applying to "
            "thrown away. Whether a language is required is the hardest rule: right on 3 of 5.",
        ],
        "real": [
            "The candidate's own decisions as labels: what was sent against what was skipped, compared from 20 "
            "decisions on.",
            "A week of real postings labelled blind, to measure the market instead of written cases.",
        ],
        "checked": "380 offline tests; the benchmark runs at every change with a floor on the tuning set, so a rule "
                   "that makes the scorer worse fails the build; the held-out set is replaced before the next figures "
                   "are published.",
        "links": [("Try the dashboard", f"{SITE}/job-search-agent/demo/"),
                  ("How the scoring is measured", f"{REPO}/job-search-agent#measured-not-asserted")],
        "skills": ["Evaluation design", "Rules engines", "Python, no dependencies", "Data pipelines", "Recruitment"],
    },
    {
        "slug": "job-search-agent-it",
        "repo": "job-search-agent",
        "lang": "it",
        "translation": "job-search-agent",
        "media": ("jsa", "La dashboard: i ruoli che valgono un'ora, perché uno ha 94, ogni annuncio con il suo verdetto "
                         "e il funnel delle candidature."),
        "tag": "Automazione · Selezione",
        "title": "Quali annunci meritano una candidatura?",
        "as_of": "15 novembre 2026",
        "client": "Chi cerca lavoro nelle risorse umane in Europa, con più annunci che sere. Le cifre sono misurate "
                  "su un candidato inventato, così si possono pubblicare.",
        "question": "Quali annunci di questa settimana meritano una candidatura, e quanto ci si può fidare di un "
                    "punteggio che lo decide?",
        "did": [
            "Ho raccolto gli annunci dalle API pubbliche di otto sistemi di selezione e da due aggregatori, con ogni "
            "fonte verificata senza rete su una risposta registrata.",
            "Ho dato a ogni annuncio un punteggio per ciascun posizionamento con regole leggibili: prima i requisiti "
            "che escludono (una lingua davvero richiesta, gli anni chiesti, il luogo, il livello, le condizioni), poi "
            "le parole chiave, con ogni punto spiegato.",
            "Ho scritto 160 annunci etichettati candidati, forse o lascia, e ne ho tenuti da parte 30, scritti dopo "
            "l'ultima modifica alle regole, per misurare ogni versione su annunci su cui non è stata tarata.",
            "Ho consegnato una dashboard, CV e lettera che possono citare solo il profilo, e l'installazione in una "
            "riga.",
        ],
        "kpis": [("21 su 30", "annunci di verifica valutati come da etichetta, erano 15 con le prime regole"),
                 ("0 su 12", "annunci da candidatura scartati; tutti tenuti almeno da rileggere"),
                 ("15 su 15", "annunci da inviare abbinati al posizionamento giusto"),
                 ("306", "bacheche aziendali, da 8 API di selezione e 2 aggregatori")],
        "found": [
            "Le prime regole valutavano come una persona metà degli annunci di verifica: 15 su 30. Regole scritte "
            "su annunci etichettati hanno portato il risultato a 20.",
            "La versione successiva ha corretto ogni errore del suo giro e su un nuovo insieme di verifica ha fatto "
            "ancora 21 su 30, come la precedente: le regole frase per frase non generalizzavano più. Il rapporto lo "
            "dice, e cita questa cifra, non il 115 su 130 sugli annunci usati per tararle.",
            "Gli errori rimasti costano poco: tre annunci da lasciare valutati da candidatura, nessun annuncio buono "
            "buttato via. Capire se una lingua è richiesta è la regola più difficile: giusta in 3 casi su 5.",
        ],
        "real": [
            "Le decisioni del candidato come etichette: cosa ha inviato e cosa ha scartato, da 20 decisioni in su.",
            "Una settimana di annunci veri etichettati alla cieca, per misurare il mercato e non casi scritti.",
        ],
        "checked": "380 test senza rete; la misura gira a ogni modifica, e una regola che peggiora il punteggio "
                   "blocca la build; l'insieme di verifica si sostituisce prima di pubblicare nuove cifre.",
        "links": [("Prova la dashboard", f"{SITE}/job-search-agent/demo/"),
                  ("Come si misura il punteggio (inglese)", f"{REPO}/job-search-agent#measured-not-asserted")],
        "skills": ["Progettare una misura", "Motori di regole", "Python senza dipendenze", "Pipeline di dati",
                   "Selezione del personale"],
    },
]

LABELS = {
    "en": {"kind": "Case study", "all": "All case studies", "client": "Client", "did": "What I did",
           "found": "What it found", "real": "With real data", "checked": "How it is checked.",
           "repo": "The repository", "other": "Italiano",
           "foot": "Synthetic or public data; not legal, pay or investment advice. Figures as published on",
           "role": "HR advisory, people analytics, reward"},
    "it": {"kind": "Caso di studio", "all": "Tutti i casi di studio (inglese)", "client": "Cliente",
           "did": "Cosa ho fatto", "found": "Cosa ha trovato", "real": "Con dati reali",
           "checked": "Come è verificato.", "repo": "Il repository", "other": "English",
           "foot": "Dati sintetici o pubblici; non è consulenza legale, retributiva o finanziaria. Cifre pubblicate il",
           "role": "consulenza HR, people analytics, retribuzioni"},
}

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
.shot{margin:0 0 22px}.shot img{display:block;width:100%;height:auto;border-radius:14px;border:1px solid var(--line)}
.item small{color:var(--accent);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.03em}
.item strong{display:block;font:650 19px/1.25 var(--display);margin:4px 0}
.item span{color:var(--ink-soft);font-size:14px}
@media (max-width:680px){.kpis{grid-template-columns:1fr 1fr}.cols{grid-template-columns:1fr;gap:0}h1{font-size:28px}}
@page{size:A4;margin:12mm 13mm}
@media print{:root{--paper:#fff;--paper-2:#f5f5f7;--ink:#1d1d1f;--ink-soft:#424245;--muted:#6e6e73;--line:#e8e8ed;
--accent:#0066cc;--accent-wash:#eef5fd;--glow:none}body{font-size:12.4px}.page{padding:0;max-width:none}
.top .web,.shot{display:none}h1{font-size:26px;margin-top:8px}.tag{margin-top:12px}.q{font-size:14.5px;margin-bottom:14px}
.client{font-size:12.6px;margin-bottom:12px}.kpis{margin-bottom:14px}.kpi b{font-size:17px}.kpi span{font-size:10.5px}
li{margin-bottom:4px}ul{margin-bottom:12px}.check{font-size:11.6px;margin-bottom:12px}.skills{margin-bottom:12px}
.foot{margin-top:12px;padding-top:8px}.links a::after{content:" " attr(href);
font-weight:400;color:#6e6e73}}
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def shot(c: dict) -> str:
    """The case's loop from media/, on screen only: the PDF stays one page."""
    if not c.get("media"):
        return ""
    name, alt = c["media"]
    return (f'<figure class="shot"><picture><source srcset="../media/{name}.png" media="(prefers-reduced-motion: '
            f'reduce)"><img src="../media/{name}.webp" width="960" height="608" loading="lazy" alt="{esc(alt)}">'
            f'</picture></figure>\n')


def page(c: dict) -> str:
    lang = c.get("lang", "en")
    L = LABELS[lang]
    ul = lambda items: "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>"
    kpis = "".join(f'<div class="kpi"><b>{esc(v)}</b><span>{esc(t)}</span></div>' for v, t in c["kpis"])
    links = "".join(f'<a href="{esc(u)}">{esc(t)}</a>' for t, u in
                    [*c["links"], (L["repo"], f"{REPO}/{c['repo']}")])
    other = (f' · <a href="{c["translation"]}.html" hreflang="{"en" if lang == "it" else "it"}">{L["other"]}</a>'
             if c.get("translation") else "")
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(c['title'])} · {L['kind']}</title>
<meta name="description" content="{esc(c['question'])}">
<style>{CSS}</style></head>
<body><main class="page">
<div class="top"><span>{L['kind']} · Domenico Perroni</span>
<span class="web"><a href="./">{L['all']}</a> · <a href="{c['slug']}.pdf">PDF</a>{other}</span></div>
<span class="tag">{esc(c['tag'])}</span>
<h1>{esc(c['title'])}</h1>
<p class="client"><b>{L['client']}:</b> {esc(c['client'])}</p>
<p class="q">{esc(c['question'])}</p>
<div class="kpis">{kpis}</div>
{shot(c)}<div class="cols">
<section><h2>{L['did']}</h2>{ul(c['did'])}</section>
<section><h2>{L['found']}</h2>{ul(c['found'])}<h2>{L['real']}</h2>{ul(c['real'])}</section>
</div>
<p class="check"><b>{L['checked']}</b> {esc(c['checked'])}</p>
<div class="skills">{"".join(f"<span>{esc(s)}</span>" for s in c['skills'])}</div>
<div class="links">{links}</div>
<p class="foot">{L['foot']}
{c.get('as_of', AS_OF)}. Domenico Perroni · {L['role']} · Kraków ·
<a href="{SITE}/">d0m3n1c0x.github.io</a></p>
</main></body></html>
"""


NUMBERS = "zero one two three four five six seven eight nine ten eleven twelve".split()


def index() -> str:
    shown = [c for c in CASES if c.get("lang", "en") == "en"]
    count = NUMBERS[len(shown)] if len(shown) < len(NUMBERS) else str(len(shown))
    items = "".join(f'<a class="item" href="{c["slug"]}.html"><small>{esc(c["tag"])}</small>'
                    f'<strong>{esc(c["title"])}</strong><span>{esc(c["question"])}</span></a>' for c in shown)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Case studies · Domenico Perroni</title>
<meta name="description" content="{count.capitalize()} one-page case studies: the question, what was done, what it found.">
<meta property="og:type" content="website">
<meta property="og:title" content="Case studies · Domenico Perroni">
<meta property="og:description" content="{count.capitalize()} client questions, one page each: what was done, what it found and what real data would change.">
<meta property="og:url" content="https://d0m3n1c0x.github.io/cases/">
<meta property="og:image" content="https://d0m3n1c0x.github.io/media/og-cases.png">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="640">
<meta property="og:image:alt" content="{count.capitalize()} client questions, one page each; 6,300 values reconciled between Excel and Python.">
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
