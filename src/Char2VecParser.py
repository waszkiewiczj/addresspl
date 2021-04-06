class Char2VecParser:
    def __init__(self):
        self.model = c2v.load_model('eng_100')

    def vectorize(self, words: List[str]) -> List:
        return self.model.vectorize_words(words)