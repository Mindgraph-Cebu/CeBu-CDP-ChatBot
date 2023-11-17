from langchainapp import airline_chat,technician_chat
from flask import Flask, Response, jsonify, request
import pandas as pd
from flask_cors import CORS
import json

app = Flask(__name__)

CORS(app,origins="*")

@app.route('/askme/airline', methods = ['GET'])
def get_airline_response():

    try:
    
        prompt = request.args.get("data")
        data = {}
          
        
        data["answer"] = airline_chat(prompt)   
        
        
        return jsonify(data)
    
    except ValueError:
        return jsonify({'answer':"Please ask questions about the database"})
    

@app.route('/askme/technician', methods = ['GET'])
def get_technician_response():

    try:
    
        prompt = request.args.get("data")
        data = {}
          
        
        data["answer"] = technician_chat(prompt)   
         
        
        return jsonify(data)
    
    except ValueError:
        return jsonify({'answer':"Please ask questions about the database"})
    


if __name__ =="__main__":
    app.run(host='0.0.0.0',port=8080)
    
    
