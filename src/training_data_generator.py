import pandas as pd
import random

from src.address_noise_generator import AddressNoiseGenerator


class TrainingDataGenerator:
    def __init__(self, address_noise_generator: AddressNoiseGenerator):
        self.address_noise_generator = address_noise_generator
        self.matches_add_noise_probability = 0.6
        self.nonmatches_add_noise_probability = 0.1

    def generate_training_data(self, addresses: pd.Series) -> pd.DataFrame:
        return pd.concat([self.generate_matches(addresses), self.generate_non_matches(addresses)])

    def generate_matches(self, addresses: pd.Series) -> pd.DataFrame:
        matches = pd.DataFrame({
            'x1': addresses,
            'x2': addresses.apply(lambda x: self.address_noise_generator.generate_noised_address(x, 
            self.matches_add_noise_probability))
        })
        matches['y'] = 0
        return matches

    def generate_non_matches(self, addresses: pd.Series) -> pd.DataFrame:
        non_matches = pd.DataFrame({
            'x1': addresses,
            'x2': self.create_non_match_data(addresses)
        })
        non_matches['y'] = 1
        return non_matches

    def create_non_match_data(self, addresses: pd.Series) -> list[str]:
        x2s = []
        len_concats = len(addresses)

        for i in range(len_concats):
            address = addresses[i]
            address_pair = address[:]
            while address_pair == address:
                address_pair = addresses[random.randrange(len_concats)]
            address_pair = self.address_noise_generator.generate_noised_address(
                address_pair, self.nonmatches_add_noise_probability)
            x2s.append(address_pair)
        return x2s
