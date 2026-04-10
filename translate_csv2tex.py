#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


LATEX_ESCAPE_MAP = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex(text: str) -> str:
    return "".join(LATEX_ESCAPE_MAP.get(ch, ch) for ch in text)


def read_csv(path: Path, encoding: str) -> list[list[str]]:
    with path.open("r", encoding=encoding, newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise ValueError("CSV is empty.")

    max_cols = max(len(row) for row in rows)
    return [row + [""] * (max_cols - len(row)) for row in rows]


def build_table(
    rows: list[list[str]],
    caption: str | None,
    label: str | None,
    column_format: str | None,
    escape: bool,
) -> str:
    cols = len(rows[0])
    colfmt = column_format or ("|" + "|".join(["c"] * cols) + "|")

    def normalize(cell: str) -> str:
        return escape_latex(cell) if escape else cell

    lines = [
        r"\begin{table}[H]",
        r"    \centering",
    ]
    if caption:
        lines.append(f"    \\caption{{{normalize(caption)}}}")
    if label:
        lines.append(f"    \\label{{{normalize(label)}}}")
    lines.append(f"    \\begin{{tabular}}{{{colfmt}}}")
    lines.append(r"        \hline")

    for row in rows:
        lines.append("        " + " & ".join(normalize(cell) for cell in row) + r" \\")
        lines.append(r"        \hline")

    lines.append(r"    \end{tabular}")
    lines.append(r"\end{table}")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Translate CSV to a basic LaTeX table.")
    parser.add_argument("input_csv", type=Path, help="Input CSV file path.")
    parser.add_argument("-o", "--output", type=Path, help="Output TeX file path. Defaults to stdout.")
    parser.add_argument("--caption", type=str, help="Table caption.")
    parser.add_argument("--label", type=str, help="Table label.")
    parser.add_argument("--column-format", type=str, help=r'LaTeX tabular column format, e.g. "|c|c|c|".')
    parser.add_argument("--encoding", type=str, default="utf-8", help="CSV file encoding (default: utf-8).")
    parser.add_argument(
        "--no-escape",
        action="store_true",
        help="Disable LaTeX escaping for cell text/caption/label.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_csv(args.input_csv, args.encoding)
    tex = build_table(
        rows=rows,
        caption=args.caption,
        label=args.label,
        column_format=args.column_format,
        escape=not args.no_escape,
    )

    if args.output:
        args.output.write_text(tex, encoding="utf-8")
    else:
        print(tex, end="")


if __name__ == "__main__":
    main()
