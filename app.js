const LATEX_ESCAPE_MAP = {
  "\\": "\\textbackslash{}",
  "&": "\\&",
  "%": "\\%",
  "$": "\\$",
  "#": "\\#",
  "_": "\\_",
  "{": "\\{",
  "}": "\\}",
  "~": "\\textasciitilde{}",
  "^": "\\textasciicircum{}",
};

function escapeLatex(text) {
  return [...text].map((ch) => LATEX_ESCAPE_MAP[ch] ?? ch).join("");
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];

    if (ch === '"') {
      if (inQuotes && next === '"') {
        cell += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
      continue;
    }

    if (!inQuotes && ch === ",") {
      row.push(cell);
      cell = "";
      continue;
    }

    if (!inQuotes && (ch === "\n" || ch === "\r")) {
      if (ch === "\r" && next === "\n") i += 1;
      row.push(cell);
      rows.push(row);
      row = [];
      cell = "";
      continue;
    }

    cell += ch;
  }

  if (cell.length > 0 || row.length > 0) {
    row.push(cell);
    rows.push(row);
  }

  if (!rows.length) {
    throw new Error("CSV is empty.");
  }

  const maxCols = Math.max(...rows.map((r) => r.length));
  return rows.map((r) => [...r, ...Array(maxCols - r.length).fill("")]);
}

function buildTable(rows, caption, label, columnFormat, shouldEscape) {
  const normalize = (t) => (shouldEscape ? escapeLatex(t) : t);
  const colfmt = columnFormat || `|${Array(rows[0].length).fill("c").join("|")}|`;
  const lines = ["\\begin{table}[H]", "    \\centering"];

  if (caption) lines.push(`    \\caption{${normalize(caption)}}`);
  if (label) lines.push(`    \\label{${normalize(label)}}`);
  lines.push(`    \\begin{tabular}{${colfmt}}`);
  lines.push("        \\hline");

  rows.forEach((r) => {
    lines.push(`        ${r.map((c) => normalize(c)).join(" & ")} \\\\`);
    lines.push("        \\hline");
  });

  lines.push("    \\end{tabular}");
  lines.push("\\end{table}");
  return `${lines.join("\n")}\n`;
}

async function onGenerate() {
  const fileInput = document.getElementById("csvFile");
  const caption = document.getElementById("caption").value.trim();
  const label = document.getElementById("label").value.trim();
  const columnFormat = document.getElementById("columnFormat").value.trim();
  const shouldEscape = document.getElementById("escapeLatex").checked;
  const output = document.getElementById("output");

  const file = fileInput.files?.[0];
  if (!file) {
    output.value = "CSVファイルを選択してください。";
    return;
  }

  try {
    const csvText = await file.text();
    const rows = parseCsv(csvText);
    output.value = buildTable(rows, caption, label, columnFormat, shouldEscape);
  } catch (err) {
    output.value = `エラー: ${err instanceof Error ? err.message : String(err)}`;
  }
}

document.getElementById("generateBtn").addEventListener("click", onGenerate);
