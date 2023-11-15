from langchainapp import airline_chat,sales_chat
from flask import Flask, Response, jsonify, request
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)

CORS(app,origins="*")

@app.route('/askme/airline', methods = ['GET'])
def get_airline_response():

    try:
    
        prompt = request.args.get("data")
        data = {"answer": airline_chat(prompt)}
  
        # print(data) 
        return jsonify(data)
    
    except ValueError:
        return jsonify({'answer':"Please ask questions about the database"})
    

@app.route('/askme/sales', methods = ['GET'])
def get_sales_response():

    try:
    
        prompt = request.args.get("data")
        data = {"answer": sales_chat(prompt)}
        # print(data) 
        
        return jsonify(data)
    
    except ValueError:
        return jsonify({'answer':"Please ask questions about the database"})
    


if __name__ =="__main__":
    app.run(host='0.0.0.0',port=8080)
    
    
