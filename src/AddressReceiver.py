import re
from annoy import AnnoyIndex
from InputCleaner import InputCleaner
from Char2VecParser import Char2VecParser
import pandas as pd

class AddressReceiver:
    def __init__(annoyTree, addressesCsv):
        self.addresses = pd.read_csv(addressesCsv, delimiter=";", encoding="utf-8")
        self.annoyTree = annoyTree
        self.cleaner = InputCleaner()
        self.char2vecParser = Char2VecParser()

    def getNiceAddress(self, inputStr):
        cleaned = cleaner.cleanInput(inputStr)

        postalCode = getPostalCode(inputStr)
        if postalCode is not None:
            cleaned = cleaned.replace(postalCode, "")

        bestAddress = self.getBestAddress(cleaned)
        return bestAddress.to_json(orient="split")

    def getBestAddress(self, inputStr):
        vector = self.char2vecParser.vectorize([inputStr])[0]
        ind = resultself.annoyTree.get_nns_by_vector(vector, 1)

        return self.addresses[ind, 1:]

    def getPostalCode(self, inputStr):
        postalCodeRegex = r"\d{2}-?\d{3}"
        postalCode = None
        match = re.search(postalCodeRegex, inputStr)
        if match is not None:
            postalCode = match.group()

        return postalCode