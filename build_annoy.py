"""
Build ANNOY tree based on input CSV.

Usage:
    build_annoy.py --csv-path CSV_PATH \
    --col-name COLUMN_NAME \
    --out OUT_PATH \
    [--model-path MODEL_PATH] \
    [--dim DIMENSION]

Options:
    --csv-path CSV_PATH
    Path to CSV file
    --col-name COLUMN_NAME
    Name of column to make embeddings from
    --out OUT_PATH
    Path to output tree file
    --model-path MODEL_PATH
    Path to custom c2v model
    --dim DIMENSION
    Number of dimension for output embeddings [default: 100]
"""

import pandas as pd
import logging
import sys

from docopt import docopt
from src.c2v_parser import Chars2VecParser
from src.annoy_builder import AnnoyBuilder


def main(csv_path: str, column_name: str, out_path: str, model_path: str, dim: int):
    parser = Chars2VecParser(model_path=model_path, embedding_size=dim)
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
        out_path=arguments["--out"],
        model_path=arguments["--model-path"],
        dim=int(arguments["--dim"])
    )
