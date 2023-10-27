import pandas as pd
import pandasai
from pandasai.llm import AzureOpenAI
from pandasai import SmartDataframe




df = pd.read_excel("data/short.xlsx")

llm = AzureOpenAI(
    api_version="2023-07-01-preview",
    api_token="2dd4400d079a4fd49ddd2e864802522a",
    api_base="https://genai-interns.openai.azure.com/",
    deployment_name="genai",
    is_chat_model=True
)

user_defined_path = "chart.png"


sdf = SmartDataframe(df, config={
                    "llm": llm,
                    "enable_cache": False,
                    "verbose": True,
                    "enforce_privacy": False,
                    # "conversational": True ,
                    "save_charts": True
                    # "save_charts_path": user_defined_path
                    }
)


response = sdf.chat("give me the points for a piechart for the revenue in years")

# print(response)
        

