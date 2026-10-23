// node design/tests/xlsx.test.mjs [file.xlsx ...]  — reads real workbooks and round-trips a written one.
import { readFileSync, writeFileSync } from "node:fs";
import { readXlsx, writeXlsx } from "../xlsx.js";

let failures = 0;
const check = (ok, what) => { if (!ok) { failures++; console.error("FAIL", what); } };

for (const path of process.argv.slice(2)) {
  const sheets = await readXlsx(readFileSync(path));
  console.log(path.split("/").pop(), sheets.map((s) => `${s.name}:${s.rows.length}`).join(" "));
}

const rows = [["matricola", "importo", "data", "ok", "nota"], ["A001", 1234.5, "2026-02-18", true, "à & <b>"], ["A002", 7, "", false, ""]];
const bytes = writeXlsx([{ name: "Segnalazioni", rows, widths: [12, 12, 12, 6, 20] }, { name: "Altro", rows: [["x"], [1]] }]);
writeFileSync(process.env.OUT || "/tmp/roundtrip.xlsx", bytes);
const back = await readXlsx(bytes);
check(back.length === 2 && back[0].name === "Segnalazioni", "sheet names");
check(JSON.stringify(back[0].rows[1]) === JSON.stringify(["A001", 1234.5, "2026-02-18", true, "à & <b>"]), `row 1: ${JSON.stringify(back[0].rows[1])}`);
check(back[0].rows[2][0] === "A002" && back[0].rows[2][1] === 7 && back[0].rows[2][3] === false, `row 2: ${JSON.stringify(back[0].rows[2])}`);
check(JSON.stringify(writeXlsx([{ name: "a", rows }])) === JSON.stringify(writeXlsx([{ name: "a", rows }])), "deterministic bytes");
console.log(failures ? `${failures} failures` : "xlsx: all checks pass");
process.exit(failures ? 1 : 0);
