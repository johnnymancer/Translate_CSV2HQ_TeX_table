import argparse
import sys
import pandas as pd
import numpy as np

def csv_to_tex(input_file, output_file=None, separator=',', na_rep='-', float_format=None, caption=None, label=None):
    try:
        df = pd.read_csv(input_file, sep=separator)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    # 旧バージョンのDataFrame.to_latexではなく、pandas >= 2.0で推奨されているStylerオブジェクトを使用します。
    # StylerはLaTeX出力に対してより柔軟な制御（例えば、インデックスの非表示など）が可能です。
    # ここでは、CSVファイルの行番号に該当するインデックス列を非表示(hide)にしています。
    styler = df.style.hide(axis="index")

    # 小数点以下の表示桁数(float_format)や、欠損値(na_rep)の表示設定を適用します。
    if float_format is not None:
        styler = styler.format(precision=float_format, na_rep=na_rep)
    else:
        styler = styler.format(na_rep=na_rep)

    # デフォルトのLaTeX環境で縦線付きの表を作成するため、列のフォーマットを生成します。
    # 例: 3列の場合 "|c|c|c|" のような文字列を作成します。
    num_cols = len(df.columns)
    col_format = "|" + "|".join(["c"] * num_cols) + "|"

    # ユーザー環境に合わせ、追加のパッケージ（booktabs等）を必要としないクラシックな表を出力します。
    # Pandas Stylerの仕様上、hrules=True を指定するとデフォルトで \toprule, \midrule, \bottomrule が出力されてしまうため、
    # 一旦この設定で文字列を生成し、後段の処理でこれらを \hline に置換します。
    tex_str = styler.to_latex(
        environment="table",       # \begin{table} ... \end{table} の環境を使用する
        caption=caption,           # 表のキャプション (\caption)
        label=label,               # 相互参照用のラベル (\label)
        column_format=col_format,  # 列の揃え方と縦線の指定 (例: |c|c|c|)
        hrules=True,               # 上下とヘッダー下の横線を有効化 (後で \hline に置換)
        position="H",              # [H] を指定し、LaTeXコード内での厳密な配置位置を指定
        position_float="centering" # 表全体を中央揃え (\centering)
    )

    # booktabsパッケージ固有のコマンドを、標準のLaTeXコマンドである \hline に置換します。
    tex_str = tex_str.replace("\\toprule", "\\hline")
    tex_str = tex_str.replace("\\midrule", "\\hline")
    tex_str = tex_str.replace("\\bottomrule", "\\hline")

    if output_file:
        # 出力ファイルが指定されている場合、生成したLaTeXコードをファイルに書き込みます。
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(tex_str)
            print(f"Successfully wrote TeX table to {output_file}")
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # 出力ファイルが指定されていない場合は、標準出力（画面）に直接出力します。
        print(tex_str)

def main():
    # argparseを使用してコマンドライン引数を定義・パースします。
    parser = argparse.ArgumentParser(description="CSVデータをLaTeXのデフォルト環境でコンパイル可能な表に変換します。")
    parser.add_argument("input", help="入力するCSVファイルのパス")
    parser.add_argument("-o", "--output", help="出力するTeXファイルのパス (指定しない場合は標準出力)", default=None)
    parser.add_argument("-d", "--digits", type=int, help="数値を丸める小数点以下の桁数", default=None)
    parser.add_argument("-c", "--caption", help="表のキャプション (\\caption)", default=None)
    parser.add_argument("-l", "--label", help="表のラベル (\\label)", default=None)
    parser.add_argument("-s", "--separator", help="CSVの区切り文字 (デフォルト: ',')", default=",")
    parser.add_argument("--na_rep", help="欠損値(空欄など)の文字列表現 (デフォルト: '-')", default="-")

    args = parser.parse_args()

    float_format = args.digits

    csv_to_tex(
        input_file=args.input,
        output_file=args.output,
        separator=args.separator,
        na_rep=args.na_rep,
        float_format=float_format,
        caption=args.caption,
        label=args.label
    )

if __name__ == "__main__":
    main()
