const LATEX_ESCAPE_MAP = {
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
  let placeholder = "\uE000";
  while (text.includes(placeholder)) {
    placeholder += "\uE000";
  }
  let escaped = [...text].map((ch) => (ch === "\\" ? placeholder : (LATEX_ESCAPE_MAP[ch] ?? ch))).join("");
  escaped = escaped.replaceAll(placeholder, "\\textbackslash{}");
  return escaped;
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

  const normalizedRows = rows.filter((r) => r.length > 0);
  if (!normalizedRows.length) {
    throw new Error("CSV is empty.");
  }

  const maxCols = Math.max(...normalizedRows.map((r) => r.length));
  return normalizedRows.map((r) => [...r, ...Array(maxCols - r.length).fill("")]);
}

function buildTable(rows, caption, label, columnFormat, shouldEscape) {
  if (!rows.length) {
    throw new Error("No rows to process.");
  }
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
  const outputs = document.getElementById("outputs");

  const files = Array.from(fileInput.files ?? []);
  if (!files.length) {
    outputs.innerHTML = '<p class="status-message">CSVファイルを選択してください。</p>';
    return;
  }

  outputs.innerHTML = "";

  const settledResults = await Promise.allSettled(files.map(async (file) => {
    const csvText = await file.text();
    const rows = parseCsv(csvText);
    return {
      fileName: file.name,
      content: buildTable(rows, caption, label, columnFormat, shouldEscape),
      isError: false,
    };
  }));

  const results = settledResults.map((result, index) => {
    if (result.status === "fulfilled") {
      return result.value;
    }
    return {
      fileName: files[index].name,
      content: `エラー: ${result.reason instanceof Error ? result.reason.message : String(result.reason)}`,
      isError: true,
    };
  });

  results.forEach((result, index) => {
    const wrapper = document.createElement("details");
    wrapper.className = "output-item";
    wrapper.open = index === 0;

    const summary = document.createElement("summary");
    summary.textContent = `${result.fileName}${result.isError ? "（エラー）" : ""}`;

    const textarea = document.createElement("textarea");
    textarea.rows = 14;
    textarea.readOnly = true;
    textarea.value = result.content;
    if (result.isError) {
      textarea.classList.add("error-output");
    }

    wrapper.append(summary, textarea);
    outputs.append(wrapper);
  });
}

document.getElementById("generateBtn").addEventListener("click", onGenerate);
