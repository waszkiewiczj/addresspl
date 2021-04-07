"""
Build ANNOY tree based on input CSV.

Usage:
    build_annoy.py --csv-path CSV_PATH \
    --col-name COLUMN_NAME \
    --out OUT_PATH

Options:
    --csv-path CSV_PATH
    Path to CSV file
    --col-name COLUMN_NAME
    Name of column to make embeddings from
    --out OUT_PATH
    Path to output tree file
"""

import pandas as pd
import logging
import sys

from docopt import docopt
from src.c2v_parser import Chars2VecParser
from src.annoy_builder import AnnoyBuilder


def main(csv_path: str, column_name: str, out_path: str):
    parser = Chars2VecParser()
    data = pd.read_csv(csv_path, encoding="UTF-8")
    builder = AnnoyBuilder(data, column_name, parser)
    tree = builder.build_tree()
    builder.export_tree(out_path, tree)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    arguments = docopt(__doc__)
    main(
        csv_path=arguments["--csv-path"],
        column_name=arguments["--col-name"],
        out_path=arguments["--out"]
    )
