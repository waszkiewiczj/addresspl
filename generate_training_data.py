"""
Generate training data.

Usage:
    generate_trainig_data.py --db-path DB_PATH \
    --out-path OUT_PATH

Options:
    --db-path DB_PATH
    Path to database csv with concatenated addresses
    --out-path OUT_PATH
    Path to output CSV file
"""
import pandas as pd

from docopt import docopt
from src.address_noise_generator import AddressNoiseGenerator
from src.training_data_generator import TrainingDataGenerator


def main(db_path: str, out_path: str):
    db = pd.read_csv(db_path)
    addresses = db['STRING']    

    address_noise_generator = AddressNoiseGenerator()
    training_data_generator = TrainingDataGenerator(address_noise_generator)

    result_df = training_data_generator.generate_training_data(addresses)

    result_df.to_csv(out_path, index=False)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(
        db_path=arguments["--db-path"],
        out_path=arguments["--out-path"]
    )
