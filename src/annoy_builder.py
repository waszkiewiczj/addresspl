import pandas as pd
import logging

from src.c2v_parser import Chars2VecParser
from annoy import AnnoyIndex
from typing import List


class AnnoyBuilder:
    def __init__(self, data_df: pd.DataFrame, data_col: str, c2v_parser: Chars2VecParser, tree_count: int = 20):
        self.data = data_df[data_col].tolist()
        self.count = len(self.data)
        self.c2v_parser = c2v_parser
        self.tree_count = tree_count
        self.logger = logging.getLogger("annoy_builder")

    def build_tree(self) -> AnnoyIndex:
        embeddings = self._get_embeddings()

        tree = AnnoyIndex(self.c2v_parser.embedding_size, "angular")
        for idx, embedding in enumerate(embeddings):
            logging.info(f"adding {idx + 1}/{self.count} vector to tree")
            tree.add_item(idx, embedding)
        tree.build(self.tree_count)

        return tree

    @staticmethod
    def export_tree(out_path: str, tree: AnnoyIndex):
        tree.save(out_path)

    def _get_embeddings(self) -> List[list]:
        embeddings = self.c2v_parser.parse(self.data, batch_size=10000)

        return embeddings
