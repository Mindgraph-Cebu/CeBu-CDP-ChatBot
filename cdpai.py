import pandas as pd
import pandasai
print(pandasai.__version__)
from pandasai.llm import AzureOpenAI, OpenAI
from pandasai import SmartDataframe

# sample data
# df = pd.DataFrame({
#     "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
#     "gdp": [19294482071552, 2891615567872, 2411255037952, 3435817336832, 1745433788416, 1181205135360, 1607402389504, 1490967855104, 4380756541440, 14631844184064],
#     "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.4, 7.23, 7.22, 5.87, 5.12]
# })

# df = pd.read_parquet("profiles/passenger_details/check_passenger.parquet")
df = pd.read_parquet("summary.parquet")

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
                    "enforce_privacy": False 
                    }
)


response = sdf.chat("which country has the highest gdp?")
print(response)

# can you give me the date of birth for the passenger_hash = fd68e562482eef0d8941437ed7ee0e4e
