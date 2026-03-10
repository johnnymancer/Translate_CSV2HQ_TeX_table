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

    # Convert numeric columns to standard format string if float_format is provided
    # pd.DataFrame.to_latex handles formatting when float_format is a function or string

    # Fill NAs if na_rep is provided, though to_latex has na_rep argument
    # Actually, let to_latex handle na_rep

    latex_kwargs = {
        'index': False,
        'escape': False, # Avoid escaping LaTeX special chars if user inputs them deliberately, though maybe safer to True. Let's use True for safety but might break math mode in CSV. Default is True in pandas 2.0+
        'na_rep': na_rep,
        'float_format': float_format
    }

    # pandas >= 2.0 recommends using Styler.to_latex, but for simplicity DataFrame.to_latex is still available or we can use Styler.
    # Styler gives better control over LaTeX output. Let's use Styler.
    styler = df.style.hide(axis="index")

    if float_format is not None:
        styler = styler.format(precision=float_format, na_rep=na_rep)
    else:
        styler = styler.format(na_rep=na_rep)

    # Determine the column format with vertical lines, e.g., |c|c|c|
    num_cols = len(df.columns)
    col_format = "|" + "|".join(["c"] * num_cols) + "|"

    # We want a classic table environment without booktabs
    tex_str = styler.to_latex(
        environment="table",
        caption=caption,
        label=label,
        column_format=col_format,
        hrules=True, # We will replace booktabs rules with \hline
        position="H",
        position_float="centering"
    )

    # Replace booktabs rules with classic \hline
    tex_str = tex_str.replace("\\toprule", "\\hline")
    tex_str = tex_str.replace("\\midrule", "\\hline")
    tex_str = tex_str.replace("\\bottomrule", "\\hline")

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
    parser = argparse.ArgumentParser(description="Convert CSV data to high-quality TeX tables.")
    parser.add_argument("input", help="Path to the input CSV file")
    parser.add_argument("-o", "--output", help="Path to the output TeX file (default: stdout)", default=None)
    parser.add_argument("-d", "--digits", type=int, help="Number of decimal digits to round to", default=None)
    parser.add_argument("-c", "--caption", help="Caption for the TeX table", default=None)
    parser.add_argument("-l", "--label", help="Label for the TeX table", default=None)
    parser.add_argument("-s", "--separator", help="Separator used in the CSV file (default: ',')", default=",")
    parser.add_argument("--na_rep", help="String representation for missing values (default: '-')", default="-")

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
