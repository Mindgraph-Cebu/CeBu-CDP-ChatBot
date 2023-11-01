from langchainapp import output
from flask import Flask, Response, jsonify, request
import pandas as pd
import json

app = Flask(__name__)


@app.route('/askme', methods = ['GET'])
def get_response():
    
    prompt = request.args.get("data")
    data = {}
    data["answer"] = output(prompt)    
    
    return jsonify(data)
    


if __name__ =="__main__":
    app.run(port=8080)
    
    
