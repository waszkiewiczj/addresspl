import random

class AddressNoiseGenerator:
    def __init__(self):
        self.model_chars = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',
               '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<',
               '=', '>', '?', '@', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
               'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
               'x', 'y', 'z', 'ą','ę','ć','ó','ź','ż','ł','ś']

    def generate_noised_address(self, address: str, add_noise_probability: float = 0.6) -> str:
        max_operations = 2
        lambdas = [lambda x: self.mix_letters(x), lambda x: self.add_letter(x), lambda x: self.replace_letter(x)]
        new_address = address[:]
        is_noised = False if random.random() > add_noise_probability else True
        if not is_noised:
            return new_address
        no_operations = random.randrange(max_operations) + 1
        for _ in range(no_operations):
            new_address = lambdas[random.randrange(len(lambdas))](new_address)
        return new_address

    def mix_letters(self, address: str) -> str:
        str_len = len(address)
        i = random.randrange(str_len - 1)
        j = random.randrange(i + 1, str_len)
        return address[:i] + address[j] + address[i+1:j] + address[i] + address[j+1:]
    
    def add_letter(self, address: str) -> str:
        return self.add_noise(address)
    
    def replace_letter(self, address: str) -> str:
        return self.add_noise(address, True)

    def add_noise(self, address: str, replace: bool = False) -> str:
        added_letter = self.model_chars[random.randrange(len(self.model_chars))]
        place_added = random.randrange(len(address))
        return address[:place_added] + added_letter + address[place_added + (1 if replace is True else 0):]