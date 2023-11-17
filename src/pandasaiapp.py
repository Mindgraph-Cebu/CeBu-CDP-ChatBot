import pandas as pd
from pandasai.llm import AzureOpenAI
from pandasai import SmartDataframe

import pandas as pd
import json


df = pd.read_excel("./passenger_Data.xlsx")

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

    
    

check = sdf.chat(" x axis months , y-axis meals . now plot the best meals consumed for each month in 2023")
        
        