# Translate_CSV2HQ_TeX_table
CSVの実験データ等を高品質なTeXテーブルに変換するツール。

## Minimal CLI

最小構成のCSV→TeX変換CLIを追加しました。

### 使い方

```bash
python /home/runner/work/Translate_CSV2HQ_TeX_table/Translate_CSV2HQ_TeX_table/translate_csv2tex.py INPUT.csv \
  -o OUTPUT.tex \
  --caption "表タイトル" \
  --label "tab:example"
```

### 主なオプション

- `--column-format`: `tabular` の列定義を指定（例: `|c|c|c|`）
- `--encoding`: CSVの文字コード（デフォルト: `utf-8`）
- `--no-escape`: LaTeXエスケープを無効化
