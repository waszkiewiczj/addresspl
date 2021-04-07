"""
Run Flask web application server

Usage:
    app.py --tree TREE \
    --data DATA

Options:
    --tree TREE
    Path to annoy tree file
    --data DATA
    Path to data CSV file
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

    parser = Chars2VecParser()
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
