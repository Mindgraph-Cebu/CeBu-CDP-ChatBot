from flask import Flask, jsonify, request
from CH_cebu_integration import get_response_clickhouse, get_response_passenger

app = Flask(__name__)

@app.route('/get_response_clickhouse', methods=['GET'])
def get_response_clickhouse_route():
    query = request.args.get('query')
    response_clickhouse = get_response_clickhouse(query)
    return jsonify({'response': response_clickhouse})

@app.route('/get_response_passenger', methods=['GET'])
def get_response_passenger_route():
    query = request.args.get('query')
    response_passenger = get_response_passenger(query)
    return jsonify({'response': response_passenger})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
