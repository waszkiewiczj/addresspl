import json

from flask import Flask, request
from typing import Dict

app = Flask(__name__)


@app.route('/', methods=['POST'])
def parse():
    data_raw = request.get_data().decode('UTF-8')
    address_list = json.loads(data_raw)
    address_list_parsed = [
        parse_address(address)
        for address in address_list
    ]
    return json.dumps(address_list_parsed)


def parse_address(address: str) -> Dict[str, str]:
    return {"raw_address": address}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
