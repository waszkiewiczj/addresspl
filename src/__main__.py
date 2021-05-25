from flask import Flask, request
from src.parsing.parsing_controller import ParsingController


if __name__ == '__main__':
    app = Flask("address_parser")
    parsing_controller = ParsingController()

    @app.route('/', methods=['POST'])
    def parse():
        raw_address = request.get_data().decode('UTF-8')
        parsed_address_list = [
            address.to_json()
            for address in parsing_controller.parse_address(raw_address)
        ]
        return f"[{','.join(parsed_address_list)}]".encode('UTF-8')

    app.run(host='0.0.0.0', port=80)
