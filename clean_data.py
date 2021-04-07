"""
Clean input address data.

Usage:
    clean_data.py --simc-csv SIMC_CSV \
    --ulic-csv ULIC_CSV \
    --out-path OUT_PATH

Options:
    --simc-csv SIMC_CSV
    Path to CSV file with SIMC records
    --ulic-csv ULIC_CSV
    Path to CSV fil with ULIC records
    --out-path OUT_PATH
    Path to output CSV file
"""
import pandas as pd

from docopt import docopt
from src.input_cleaner import InputCleaner


def main(simc_csv: str, ulic_csv: str, out_path: str):
    csv_reader_kwargs = dict(delimiter=";")
    simc_df = pd.read_csv(simc_csv, **csv_reader_kwargs)
    ulic_df = pd.read_csv(ulic_csv, **csv_reader_kwargs)

    merged_df = ulic_df.merge(simc_df, left_on='SYM', right_on='SYM')
    merged_df = merged_df[["NAZWA", "CECHA", "NAZWA_1", "NAZWA_2"]]
    merged_df = merged_df.fillna("")

    cleaner = InputCleaner()

    concat_combinations = [
        ["NAZWA_2", "CECHA", "NAZWA_1", "NAZWA"],
        ["NAZWA", "NAZWA_2", "CECHA", "NAZWA"]
    ]
    concat_series = pd.Series()

    result_df = merged_df
    for combination in concat_combinations:
        concat_series_tmp = merged_df[combination[0]].map(str)
        for combination_el in combination[1:]:
            concat_series_tmp = concat_series_tmp + merged_df[combination_el].map(str)
        concat_series = concat_series.append(concat_series_tmp)
        merged_df = result_df.append(merged_df)

    concat_series = concat_series.apply(cleaner.clean_input)

    result_df = merged_df.append(merged_df)
    result_df["STRING"] = concat_series
    result_df.to_csv(out_path, index=False)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(
        simc_csv=arguments["--simc-csv"],
        ulic_csv=arguments["--ulic-csv"],
        out_path=arguments["--out-path"]
    )
