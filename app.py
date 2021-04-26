"""
Run Flask web application server

Usage:
    app.py --tree TREE \
    --data DATA \
    [--model-path MODEL_PATH] \
    [--dim DIMENSION]

Options:
    --tree TREE
    Path to annoy tree file
    --data DATA
    Path to data CSV file
    --model-path MODEL_PATH
    Path to custom c2v model
    --dim DIMENSION
    Number of dimension for output embeddings [default: 100]
"""
import json
import pandas as pd

from docopt import docopt
from flask import Flask, request
from typing import Dict
from annoy import AnnoyIndex
from src.address_receiver import AddressReceiver
from src.c2v_parser import Chars2VecParser
from src.input_cleaner import InputCleaner


if __name__ == '__main__':
    arguments = docopt(__doc__)

    parser = Chars2VecParser(model_path=arguments["--model-path"], embedding_size=int(arguments["--dim"]))
    data = pd.read_csv(arguments["--data"])
    cleaner = InputCleaner()
    tree = AnnoyIndex(parser.embedding_size, 'angular')
    tree.load(arguments["--tree"])
    receiver = AddressReceiver(tree, data, cleaner, parser)

    app = Flask(__name__)

    def parse_address(address: str) -> Dict[str, str]:
        nice_address = receiver.get_pretty_address(address)
        return nice_address

    @app.route('/', methods=['POST'])
    def parse():
        data_raw = request.get_data().decode('UTF-8')
        address_list = json.loads(data_raw)
        address_list_parsed = [
            parse_address(address)
            for address in address_list
        ]
        return json.dumps(address_list_parsed, ensure_ascii=False).encode('UTF-8')

    app.run(host='0.0.0.0', port=80)
