import pandas as pd
import pandasai
from pandasai.llm import AzureOpenAI
from pandasai import SmartDataframe

from flask import Flask, Response, jsonify, request
import pandas as pd
import json

app = Flask(__name__)

df = pd.read_excel("short.xlsx")

llm = AzureOpenAI(
    api_version="2023-07-01-preview",
    api_token="2dd4400d079a4fd49ddd2e864802522a",
    api_base="https://genai-interns.openai.azure.com/",
    deployment_name="genai",
    is_chat_model=True
)



sdf = SmartDataframe(df, config={
                    "llm": llm,
                    "enable_cache": False,
                    "verbose": True,
                    "enforce_privacy": False,
                    "conversational": True
                    }
)

@app.route('/askme', methods = ['GET'])
def get_response():
    
    
    prompt = request.args.get("prompt").split("_")
    
    new_str = ""
    
    for i in prompt:
        new_str += i
        new_str += "_"
    
    try:
        response = sdf.chat(new_str)
        
        new_dict = {}
        
        new_dict["answer"] = response
    
        return jsonify(new_dict)
    
    except Exception:
        
        result = "Sorry , I was not able to find any relevant results"
    
        new_dict = {}
        
        new_dict["answer"] = result
    
        return jsonify(new_dict)


if __name__ =="__main__":
    app.run(port=8080)
