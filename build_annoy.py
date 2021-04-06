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
import chars2vec as c2v

from docopt import docopt
from annoy import AnnoyIndex
from typing import List


class Char2VecParser:
    def __init__(self):
        self.model = c2v.load_model('eng_100')

    def vectorize(self, words: List[str]) -> List:
        return self.model.vectorize_words(words)


def build_annoy(csv_path: str, column_name: str, out_path: str):
    data = pd.read_csv(csv_path)
    str_data = data[column_name].tolist()
    embeddings = Char2VecParser().vectorize(str_data)
    count = len(embeddings)
    annoy_idx = AnnoyIndex(count, 'angular')
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
