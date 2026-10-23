# strumenti-design

The shared base of the portfolio's browser tools: one look, two languages, and the plumbing every tool needs to
work on the user's own files without sending them anywhere.

| File | What it gives a tool |
|---|---|
| `strumenti.css` | The look: system font, spacing, cards, a drop zone for files, buttons at least 44px tall, tables, light and dark from the system setting, print styles |
| `i18n.js` | Italian and English in the same page, remembered on the device; numbers, money and percentages in the right format |
| `table.js` | A CSV or Excel file turned into rows; its columns matched to the ones the tool needs, by name or alias, with the user's choices remembered |
| `xlsx.js` | Excel files read and written in the page, with no library: an .xlsx is a zip of XML, and the browser can inflate zip entries itself |

## Rules every tool follows

1. **The user's file never leaves the computer.** No upload, no server, no script from another site on the tool
   page. Each tool says so on screen, and it can be checked by going offline after the page has loaded.
2. **Plain words.** Every screen explains what to do next in a sentence; technical terms only where the user's own
   job uses them.
3. **Both languages, everywhere**: interface, messages, downloaded files.
4. **Large, visible, reachable**: targets of at least 44px, a visible focus ring, works with the keyboard alone and
   at 200% zoom.

## Using it in a tool

Each tool keeps its own copy in `web/design/`, so its page works on its own and offline. Copy the four files, keep
the version line at the top of each, and update all four together.

```html
<link rel="stylesheet" href="design/strumenti.css">
<script type="module">
  import { createI18n } from "./design/i18n.js";
  import { readTable, matchColumns } from "./design/table.js";
</script>
```

## Tests

`node design/tests/table.test.mjs` and `node design/tests/xlsx.test.mjs` (the second also round-trips a workbook
and reads real ones passed as arguments). CI runs both and opens the written workbook with openpyxl.
