# Translate_CSV2HQ_TeX_table
CSVの実験データ等を高品質なTeXテーブルに変換するツール。

## Web App (Minimal)

Python CLIではなく、ブラウザ上で動く最小Webアプリ構成に移植しました。

### 使い方

```bash
npm start
```

ブラウザで `http://localhost:5173` を開き、CSVを選択してTeXを生成します。

### 入力項目

- Caption
- Label
- Column format（例: `|c|c|c|`）
- LaTeXエスケープ有効/無効
