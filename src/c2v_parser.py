import chars2vec as c2v

from typing import List


class Chars2VecParser:
    def __init__(self, embedding_size: int = 100):
        assert embedding_size in (50, 100, 150, 300), "not supported embedding size"
        self.embedding_size = embedding_size
        self.model = c2v.load_model(f"eng_{self.embedding_size}")

    def parse(self, words: List[str]) -> List:
        return self.model.vectorize_words(words)

    def parse_single(self, word: str) -> str:
        return self.model.vectorize_words([word])[0]
