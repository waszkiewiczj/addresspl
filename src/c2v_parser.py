import chars2vec as c2v
import logging

from typing import List


class Chars2VecParser:
    def __init__(self, embedding_size: int = 100):
        assert embedding_size in (50, 100, 150, 300), "not supported embedding size"
        self.embedding_size = embedding_size
        self.model = c2v.load_model(f"eng_{self.embedding_size}")
        self.logger = logging.getLogger("Chars2VecParser")

    def parse(self, words: List[str], batch_size: int = None) -> List:
        if batch_size:
            self.logger.info(f"Processing data in batches of {batch_size} records")
            parsed_words = []
            count = len(words)
            batches = [
                words[it:(it + batch_size)]
                for it in range(0, count, batch_size)
            ]
            for n, batch in enumerate(batches):
                self.logger.info(f"Processing {n + 1}/{len(batches)} batch")
                parsed_batch = self.model.vectorize_words(batch).tolist()
                parsed_words = parsed_words + parsed_batch
        else:
            self.logger.info("No batch size set, converting all records in one run")
            parsed_words = self.model.vectorize_words(words)

        return parsed_words

    def parse_single(self, word: str) -> str:
        return self.model.vectorize_words([word])[0]
