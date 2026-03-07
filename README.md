# Translate_CSV2HQ_TeX_table

CSVの実験データ等を高品質なTeXテーブルに変換するコマンドラインツール。
pandasを活用し、学術論文（特にTeX）でそのまま使用できる見栄えの良いテーブルのLaTeXコードを自動生成します。
`booktabs` スタイル（`\toprule`, `\midrule`, `\bottomrule`）の罫線を使用します。

## 主な機能

- 高品質なTeX出力（`booktabs`対応）
- 数値の自動フォーマット（小数点以下の桁数指定）
- 柔軟なCSV読み込み（区切り文字の指定、欠損値のハイフン等への自動変換）
- テーブルメタデータ（キャプション、ラベル）の自動生成

## 必要要件

- Python 3.x
- pandas
- jinja2

## インストール

依存パッケージをインストールします：

```bash
pip install -r requirements.txt
```

## 使い方

ターミナルから以下のように実行します。

### 基本的な使い方

標準出力にTeXコードを出力します。

```bash
python csv2tex.py input.csv
```

### オプションの指定

出力ファイルの指定、小数点以下2桁への丸め、キャプション、ラベルを指定する例です。

```bash
python csv2tex.py input.csv -o output.tex --digits 2 --caption "実験結果の比較" --label "tab:results"
```

### オプション一覧

- `input`: 入力CSVファイルのパス
- `-o`, `--output`: 出力するTeXファイルのパス（デフォルト: 標準出力）
- `-d`, `--digits`: 小数点以下の表示桁数
- `-c`, `--caption`: TeXテーブルのキャプション（`\caption{}`）
- `-l`, `--label`: TeXテーブルのラベル（`\label{}`）
- `-s`, `--separator`: CSVの区切り文字（デフォルト: `,`）
- `--na_rep`: 欠損値の文字列表現（デフォルト: `-`）

## 出力されるTeXコードの例

生成されたTeXコードを使用するためには、メインのTeXファイルにて `\usepackage{booktabs}` を宣言してください。

```latex
\begin{table}[htbp]
\centering
\caption{実験結果の比較}
\label{tab:results}
\begin{tabular}{lrrr}
\toprule
Method & Accuracy & Precision & Recall \\
\midrule
Baseline & 0.85 & 0.82 & 0.88 \\
Ours & 0.92 & 0.90 & 0.94 \\
Other & - & 0.70 & 0.75 \\
\bottomrule
\end{tabular}
\end{table}
```
