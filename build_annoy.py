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

from docopt import docopt
from annoy import AnnoyIndex
from src.Char2VecParser import Char2VecParser


def build_annoy(csv_path: str, column_name: str, out_path: str):
    data = pd.read_csv(csv_path)
    word_data = data[column_name].tolist()
    count = len(word_data)

    parser = Char2VecParser()
    embeddings = []
    for idx, word in enumerate(word_data):
        print(f"vectorizing {idx + 1}/{count} row")
        emb = parser.vectorize([word])[0]
        embeddings.append(emb)

    annoy_idx = AnnoyIndex(100, 'angular')
    for idx, embedding in enumerate(embeddings):
        print(f"adding {idx + 1}/{count} to ANNOY")
        annoy_idx.add_item(idx, embedding)
    annoy_idx.build(20)
    annoy_idx.save(out_path)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    build_annoy(
        csv_path=arguments['--csv-path'],
        column_name=arguments['--col-name'],
        out_path=arguments['--out']
    )
