import pandas as pd
from pandasai.llm import AzureOpenAI
from pandasai import SmartDataframe
from clickhouse_driver import Client
from flask import Flask, Response, jsonify, request

# Initialize ClickHouse client
clickhouse_client = Client(
    host="20.213.35.159",
    port=9000,
    user="default",
    password="Neha12345",
    database="default",
)

# Check if ClickHouse client is connected
if clickhouse_client is not None:
    print("Connected to ClickHouse")
else:
    print("Failed to connect to ClickHouse")

# Load data from ClickHouse into a DataFrame
query = "SELECT * FROM CaseTable"
try:
    df = pd.DataFrame(clickhouse_client.execute(query), columns=["caseid","casetitle","description","status","priority","categorytype","reportedbycustomercustomerid","reportedbycustomerfirstname","reportedbycustomerlastname","reportedbycustomeremailaddress","reportedbycustomerphonenumber","assignedtotechniciantechnicianid","assignedtotechnicianfirstname","assignedtotechnicianlastname","assignedtotechnicianemailaddress","assignedtotechnicianphonenumber","creationdate","lastupdateddate","closeddate","resolution","attachments0filename","attachments0url","commentsnotes0author","commentsnotes0timestamp","commentsnotes0comment","relatedcustomercustomerid","relatedcustomerfirstname","relatedcustomerlastname","relatedcustomeremailaddress","relatedproductsservices0","relatedproductsservices1","customfieldscustomfield1","customfieldscustomfield2","referencesorderreference","referencestechnicianreference","audittrail0timestamp","audittrail0user","audittrail0changedescription","tagslabels0","tagslabels1","severity","duedate","location","clientinformationclientname","clientinformationclientcontact","clientinformationclientemail","clientinformationclientphone"])
    print("Data fetched successfully")
except Exception as e:
    print(f"An error occurred while fetching data: {e}")

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

app = Flask(__name__)

@app.route('/askme', methods=['GET'])
def get_response():
    prompt = request.args.get("prompt")

    if prompt is not None:
        # Split the prompt into a list of words
        prompt_list = prompt.split("_")

        new_str = ""
        for i in prompt_list:
            new_str += i
            new_str += "_"

        try:
            response = sdf.chat(new_str)

            new_dict = {}
            new_dict["answer"] = response

            return jsonify(new_dict)

        except Exception as e:
            print(f"An error occurred: {e}")
            result = "Sorry, there was an error processing your request."

    else:
        result = "Error: 'prompt' parameter not found in the query string."

    new_dict = {}
    new_dict["answer"] = result

    return jsonify(new_dict)

if __name__ =="__main__":
    app.run(port=8080)