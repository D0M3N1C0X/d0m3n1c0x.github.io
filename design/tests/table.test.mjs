// node design/tests/table.test.mjs — CSV parsing and column matching.
import { parseCsv, matchColumns, applyMapping, normalise } from "../table.js";

let failures = 0;
const eq = (a, b, what) => { if (JSON.stringify(a) !== JSON.stringify(b)) { failures++; console.error("FAIL", what, JSON.stringify(a), "!=", JSON.stringify(b)); } };

eq(normalise(" Data di Assunzione "), "data_di_assunzione", "normalise spaces and case");
eq(normalise("Città/Sede"), "citta_sede", "normalise accents and symbols");

const it = parseCsv('﻿matricola;netto;nota\r\nA001;1.234,50;"ha detto ""sì""; poi"\r\n\r\nA002;10;\n');
eq(it.headers, ["matricola", "netto", "nota"], "headers, BOM removed");
eq(it.rows.length, 2, "blank lines skipped");
eq(it.rows[0].nota, 'ha detto "sì"; poi', "quoted field with separator and quotes");
eq(it.decimalComma, true, "semicolon means decimal comma");
eq(parseCsv("a,b\n1.5,2\n").decimalComma, false, "comma separator");

const fields = [{ key: "matricola", required: true, aliases: ["codice dipendente", "id"] },
  { key: "data_assunzione", required: true, aliases: ["data di assunzione", "hire date"] },
  { key: "ratei_13", required: false, aliases: ["ratei tredicesima"] }];
const m = matchColumns(["Codice dipendente", "Data di assunzione", "Altro"], fields);
eq(m.mapping, { matricola: "Codice dipendente", data_assunzione: "Data di assunzione" }, "aliases matched");
eq(m.missing, [], "nothing required missing");
eq(matchColumns(["Codice dipendente"], fields).missing, ["data_assunzione"], "missing required");
eq(matchColumns(["X", "Y"], fields, { matricola: "X", data_assunzione: "Y" }).missing, [], "saved choices win");
eq(applyMapping([{ "Codice dipendente": "A1", Altro: 3 }], { matricola: "Codice dipendente" }), [{ matricola: "A1" }], "rows renamed");

console.log(failures ? `${failures} failures` : "table: all checks pass");
process.exit(failures ? 1 : 0);
