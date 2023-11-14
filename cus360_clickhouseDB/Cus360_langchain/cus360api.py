from flask import Flask, request, jsonify
from Clickhouse_Integration import output

app = Flask(__name__)

@app.route('/get_response', methods=['GET'])
def get_response():
    query = request.args.get('query')
    response = output(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
