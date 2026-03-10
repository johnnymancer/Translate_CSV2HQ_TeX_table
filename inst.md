# Translate_CSV2HQ_TeX_table 使用説明書

本ツールは、CSV形式のデータを読み込み、LaTeXのデフォルト環境（追加パッケージ不要）でコンパイル可能なクラシックな表（縦線および `\hline` 付き）のコードを自動生成するコマンドラインツールです。

## 1. 事前準備
Python 3.x がインストールされている環境で、以下のコマンドを実行し必要なパッケージをインストールしてください。

```bash
pip install -r requirements.txt
```

## 2. 入力可能なCSVの例
1行目にヘッダー（列名）があり、2行目以降にデータが続く一般的なCSVファイルに対応しています。

**例: `sample.csv`**
```csv
Method,Accuracy,Precision,Recall
Baseline,0.85,0.82,0.88
Ours,0.92,0.90,0.94
Other,,0.70,0.75
```
※ `Other` 行の `Accuracy` のようにデータが空欄（欠損値）になっている場合でも自動で処理されます。

## 3. 基本的な使い方
ターミナルで `csv2tex.py` に続けて変換したいCSVファイルのパスを指定して実行します。結果は標準出力（画面上）に表示されます。

```bash
python csv2tex.py sample.csv
```

## 4. オプション機能と使用例

### a. ファイルに出力する (`-o`, `--output`)
生成されたTeXコードを直接ファイルに保存したい場合に使用します。
```bash
python csv2tex.py sample.csv -o output.tex
```

### b. 小数点以下の桁数を揃える (`-d`, `--digits`)
数値データの小数点以下の表示桁数を指定して統一します。
```bash
python csv2tex.py sample.csv -d 2
```
（例: `0.85` のまま、あるいは `0.8` が `0.80` に整形されます）

### c. キャプションを追加する (`-c`, `--caption`)
表のタイトル（キャプション）を指定します。
```bash
python csv2tex.py sample.csv -c "実験結果の比較"
```

### d. ラベルを追加する (`-l`, `--label`)
本文から参照するためのラベルを指定します。
```bash
python csv2tex.py sample.csv -l "tab:result_comp"
```

### e. 欠損値の表示を変更する (`--na_rep`)
CSV内で空欄になっている部分（欠損値）をどのように表示するかを指定します。デフォルトはハイフン (`-`) です。
```bash
python csv2tex.py sample.csv --na_rep "N/A"
```

## 5. 複合例と出力結果
上記のオプションを組み合わせて実行する例です。

**実行コマンド:**
```bash
python csv2tex.py sample.csv -d 3 -c "実験結果の比較" -l "tab:results"
```

**出力されるTeXコード:**
```latex
\begin{table}[H]
\centering
\caption{実験結果の比較}
\label{tab:results}
\begin{tabular}{|c|c|c|c|}
\hline
Method & Accuracy & Precision & Recall \\
\hline
Baseline & 0.850 & 0.820 & 0.880 \\
Ours & 0.920 & 0.900 & 0.940 \\
Other & - & 0.700 & 0.750 \\
\hline
\end{tabular}
\end{table}
```
この出力結果は、追加のパッケージ（`booktabs`など）をインクルードすることなく、標準のLaTeX環境でそのままコンパイルして利用することができます。