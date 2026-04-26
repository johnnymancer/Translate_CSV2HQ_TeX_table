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
const DEFAULT_TEXTAREA_ROWS = 14;

function escapeLatex(text) {
  let counter = 0;
  let placeholder = "";
  do {
    counter += 1;
    placeholder = `__LATEX_BACKSLASH_${counter}__`;
  } while (text.includes(placeholder));
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

function renderFileOptions(files) {
  const fileOptions = document.getElementById("fileOptions");
  fileOptions.innerHTML = "";

  if (!files.length) return;

  files.forEach((file, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "file-option-item";

    const title = document.createElement("p");
    title.className = "file-option-title";
    title.textContent = file.name;

    const captionLabel = document.createElement("label");
    captionLabel.textContent = "Caption";
    const captionInput = document.createElement("input");
    captionInput.type = "text";
    captionInput.id = `caption-${index}`;
    captionInput.placeholder = "表タイトル";
    captionLabel.append(captionInput);

    const labelLabel = document.createElement("label");
    labelLabel.textContent = "Label";
    const labelInput = document.createElement("input");
    labelInput.type = "text";
    labelInput.id = `label-${index}`;
    labelInput.placeholder = "tab:example";
    labelLabel.append(labelInput);

    wrapper.append(title, captionLabel, labelLabel);
    fileOptions.append(wrapper);
  });
}

async function onGenerate() {
  const fileInput = document.getElementById("csvFile");
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
    const caption = document.getElementById(`caption-${files.indexOf(file)}`)?.value.trim() ?? "";
    const label = document.getElementById(`label-${files.indexOf(file)}`)?.value.trim() ?? "";
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
    textarea.rows = DEFAULT_TEXTAREA_ROWS;
    textarea.readOnly = true;
    textarea.value = result.content;
    if (result.isError) {
      textarea.classList.add("error-output");
    }

    wrapper.append(summary, textarea);
    outputs.append(wrapper);
  });
}

document.getElementById("csvFile").addEventListener("change", (event) => {
  const files = Array.from(event.target.files ?? []);
  renderFileOptions(files);
});
document.getElementById("generateBtn").addEventListener("click", onGenerate);
