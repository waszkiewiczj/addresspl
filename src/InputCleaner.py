import re


class InputCleaner:
    def cleanInput(self, inputStr):
        cleaned = inputStr.lower()
        cleaned = cleaned.strip()
        cleaned = self.removePolishLetters(inputStr)
        cleaned = self.replaceAddressTypesToShortcuts(inputStr)
        cleaned = re.sub(r"\s+", "", cleaned)
        cleaned = cleaned.replace(",", "")

        return cleaned

    def removePolishLetters(self, inputStr):
        lettersDict = {"ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó":"o", "ś": "s", "ź": "z", "ż": "z"}
        for plLetter, engLetter in lettersDict.items():
            inputStr = inputStr.replace(plLetter, engLetter)

        return inputStr

    def replaceAddressTypesToShortcuts(self, inputStr):
        addressTypesDict = {
            "ulca": "ul", 
            "plac": "pl"
        }

        for fullType, shortType in addressTypesDict.items():
            inputStr = inputStr.replace(fullType, shortType)

        return inputStr