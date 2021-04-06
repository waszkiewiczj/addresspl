import json

from flask import Flask, request
from typing import Dict
from src.AddressReceiver import AddressReceiver
from annoy import AnnoyIndex

app = Flask(__name__)
tree = AnnoyIndex(100, 'angular')
tree.load('data/tree.ann')
receiver = AddressReceiver(tree, 'data/db.csv')


@app.route('/', methods=['POST'])
def parse():
    data_raw = request.get_data().decode('UTF-8')
    address_list = json.loads(data_raw)
    address_list_parsed = [
        parse_address(address)
        for address in address_list
    ]
    return json.dumps(address_list_parsed, ensure_ascii=False).encode('UTF-8')


def parse_address(address: str) -> Dict[str, str]:
    nice_address = receiver.getNiceAddress(address)
    return nice_address


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
