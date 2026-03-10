import argparse
import sys
import pandas as pd
import numpy as np
import re

def create_multi_table(input_file, output_file=None, separator=',', na_rep='-', float_format=None, caption=None, label=None, header_rows=1, index_cols=0):
    """
    PandasのMultiIndexを利用してmulticolumnやmultirowに対応したクラシックなLaTeX表を出力する。
    """
    try:
        # headerとindexの指定をリスト化する（0始まりのインデックス）
        # 例: header_rows=2 なら header=[0, 1]
        header_args = list(range(header_rows)) if header_rows > 1 else 0

        # 例: index_cols=1 なら index_col=[0], index_cols=2 なら index_col=[0, 1]
        index_args = list(range(index_cols)) if index_cols > 1 else (0 if index_cols == 1 else None)

        # CSVの読み込み。MultiIndexやMultiColumnが自動生成される
        df = pd.read_csv(input_file, sep=separator, header=header_args, index_col=index_args)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    # ---------------------------------------------------------
    # フォーマットの設定
    # ---------------------------------------------------------
    # index_col が指定されていない場合は、行番号（デフォルトインデックス）を隠す
    styler = df.style
    if index_cols == 0:
        styler = styler.hide(axis="index")

    if float_format is not None:
        styler = styler.format(precision=float_format, na_rep=na_rep)
    else:
        styler = styler.format(na_rep=na_rep)

    # ---------------------------------------------------------
    # カラムフォーマット（|c|c|c|...）の生成
    # ---------------------------------------------------------
    # データ列の数
    num_data_cols = len(df.columns)

    # インデックス列の数（index_colが設定されている場合）
    num_idx_cols = index_cols

    total_cols = num_data_cols + num_idx_cols
    col_format = "|" + "|".join(["c"] * total_cols) + "|"

    # ---------------------------------------------------------
    # LaTeXコードの生成
    # ---------------------------------------------------------
    # sparse_index や clines オプションはMultiIndexやmultirowの生成に必要
    tex_str = styler.to_latex(
        environment="table",
        caption=caption,
        label=label,
        column_format=col_format,
        hrules=True,               # 横線を一旦booktabsで出力させる
        clines="all;index",        # clinesの指定
        sparse_index=True,         # multirow を有効化
        sparse_columns=True,       # multicolumn を有効化
        multirow_align="c",
        multicol_align="c|",       # 結合列のフォーマット
        position="H",
        position_float="centering"
    )

    # ---------------------------------------------------------
    # booktabs 固有コマンドの削除・置換 (クラシックな \hline へ)
    # ---------------------------------------------------------
    # to_latex(hrules=True) は \toprule, \midrule, \bottomrule を生成する。
    tex_str = tex_str.replace("\\toprule", "\\hline")
    tex_str = tex_str.replace("\\bottomrule", "\\hline")

    # \midrule については、MultiIndexヘッダーがある場合、複数出力されることがある。
    # 基本的にはすべて \hline に置換する。
    tex_str = tex_str.replace("\\midrule", "\\hline")

    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(tex_str)
            print(f"Successfully wrote TeX table to {output_file}")
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(tex_str)

def main():
    parser = argparse.ArgumentParser(description="CSVデータをLaTeXのデフォルト環境（multirow/multicolumn対応）でコンパイル可能な表に変換します。")
    parser.add_argument("input", help="入力するCSVファイルのパス")
    parser.add_argument("-o", "--output", help="出力するTeXファイルのパス (指定しない場合は標準出力)", default=None)
    parser.add_argument("-d", "--digits", type=int, help="数値を丸める小数点以下の桁数", default=None)
    parser.add_argument("-c", "--caption", help="表のキャプション (\\caption)", default=None)
    parser.add_argument("-l", "--label", help="表のラベル (\\label)", default=None)
    parser.add_argument("-s", "--separator", help="CSVの区切り文字 (デフォルト: ',')", default=",")
    parser.add_argument("--na_rep", help="欠損値(空欄など)の文字列表現 (デフォルト: '-')", default="-")

    # 新規追加オプション
    parser.add_argument("--header-rows", type=int, default=1, help="ヘッダーとして読み込む行数（multicolumnを利用する場合は2以上を指定）")
    parser.add_argument("--index-cols", type=int, default=0, help="行のインデックス（multirowによる結合対象）として読み込む左側からの列数")

    args = parser.parse_args()

    create_multi_table(
        input_file=args.input,
        output_file=args.output,
        separator=args.separator,
        na_rep=args.na_rep,
        float_format=args.digits,
        caption=args.caption,
        label=args.label,
        header_rows=args.header_rows,
        index_cols=args.index_cols
    )

if __name__ == "__main__":
    main()
