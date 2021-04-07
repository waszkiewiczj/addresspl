import re


class InputCleaner:
    def clean_input(self, input_str: str) -> str:
        cleaned = input_str.lower()
        cleaned = cleaned.strip()
        cleaned = self.remove_postal_code(cleaned)
        cleaned = self.remove_polish_letters(cleaned)
        cleaned = self.replace_address_types_to_shortcuts(cleaned)
        cleaned = self.remove_special_characters(cleaned)
        cleaned = self.remove_whitespaces(cleaned)

        return cleaned

    @staticmethod
    def remove_polish_letters(input_str: str) -> str:
        letters_dict = {"ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o", "ś": "s", "ź": "z", "ż": "z"}
        for pl_letter, eng_letter in letters_dict.items():
            input_str = input_str.replace(pl_letter, eng_letter)

        return input_str

    @staticmethod
    def replace_address_types_to_shortcuts(input_str: str) -> str:
        address_types_dict = {
            "ulca": "ul", 
            "plac": "pl"
        }

        for full_type, short_type in address_types_dict.items():
            input_str = input_str.replace(full_type, short_type)

        return input_str

    @staticmethod
    def remove_special_characters(input_str: str) -> str:
        input_str = re.sub(r"\.+|,+", "", input_str)

        return input_str

    @staticmethod
    def remove_whitespaces(input_str: str) -> str:
        input_str = re.sub(r"\s+", "", input_str)

        return input_str

    @staticmethod
    def remove_postal_code(input_str: str):
        input_str = re.sub(r"\d{2}-?\d{3}", "", input_str)

        return input_str
