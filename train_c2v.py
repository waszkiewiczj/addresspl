"""
Train on C2V model based on CSV with pairs of words.

Usage:
    train_c2v.py --csv-path CSV_PATH \
    --out-model OUT_MODEL \
    [--dim DIMENSION]

Options:
    --csv-path CSV_PATH
    Path to CSV file
    --out-model OUT_MODEL
    Path to save output model
    --dim DIMENSION
    Number of dimension for output embeddings [default: 50]
"""

import logging
import sys
import pandas as pd
import chars2vec as c2v

from docopt import docopt


def main(csv_path: str, out_model: str, dim: int):
    data = pd.read_csv(csv_path)

    X_train = data.loc[:, ["x1", "x2"]].to_numpy().tolist()
    y_train = data["y"].tolist()

    model_chars = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',
                   '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<',
                   '=', '>', '?', '@', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                   'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                   'x', 'y', 'z']

    model = c2v.train_model(dim, X_train, y_train, model_chars)
    c2v.save_model(model, out_model)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    arguments = docopt(__doc__)
    main(
        csv_path=arguments["--csv-path"],
        out_model=arguments["--out-model"],
        dim=int(arguments["--dim"])
    )
