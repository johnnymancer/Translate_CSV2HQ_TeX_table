# Translate_CSV2HQ_TeX_table

CSVの実験データ等をTeXテーブルに変換するコマンドラインツール。
pandasを活用し、LaTeXのデフォルト環境のみでコンパイル可能なテーブルのコードを自動生成します。
追加パッケージ（`booktabs`など）を必要とせず、標準の罫線（`\hline`）と縦線を使用したクラシックな表を出力します。

## 主な機能

- デフォルトのTeX環境でコンパイル可能なクラシックな表出力（縦線、`\hline`対応）
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

追加パッケージをインストールせず、標準のTeX環境でコンパイル可能です。

```latex
\begin{table}[H]
\centering
\caption{実験結果の比較}
\label{tab:results}
\begin{tabular}{|c|c|c|c|}
\hline
Method & Accuracy & Precision & Recall \\
\hline
Baseline & 0.85 & 0.82 & 0.88 \\
Ours & 0.92 & 0.90 & 0.94 \\
Other & - & 0.70 & 0.75 \\
\hline
\end{tabular}
\end{table}
```
