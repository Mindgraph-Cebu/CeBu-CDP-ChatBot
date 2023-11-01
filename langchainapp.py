from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.prompts import PromptTemplate
import duckdb
import pandas as pd

# conn = duckdb.connect(database='duckdb:///src/data.db')


uri = "sqlite:///data.db"

db = SQLDatabase.from_uri(uri)
# ,include_tables=['profile']

# df = pd.read_excel('./passenger_Data.xlsx')

llm = AzureChatOpenAI(model="gpt-35-turbo",
                      openai_api_key="2dd4400d079a4fd49ddd2e864802522a",
                      openai_api_base="https://genai-interns.openai.azure.com/",
                      deployment_name="genai",
                      openai_api_version="2023-07-01-preview",
                      temperature=0)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

template = ("""
            You are a SQL Analyst that is querying a database of a summary of a airline .
            
            Below is a description of the columns ,data types , and information in the columns:
            
            The column name Passenger_name with the data type object contains the names of the passengers
            
            The column name Arrival_station with the data type object contains the arrival station of the passenger
            
            The column name Departure_station with the data type object contains the departure station of the passenger
            
            The column name Date_of_birth with the data type DateTime contains the data of birth of the passenger
            
            The column name Gender with the data type object contains the gender of the passenger
            
            The column name Meals with the data type object contains the data of meals consumed of the passenger
            
            The column name Baggage with the data type object contains the data of Baggage consumed of the passenger
            
            The column name Revenue with the data type float64 contains the data of Revenue generated by the passenger
            
            The column name Country with the data type object contains the data of Country the passenger belongs too
            
            The column name Unique_passenger_id with the data type object contains the data of unique passenger id of the passenger
            
            The column name Travel_Date with the data type DateTime contains the data of the date travelled by the passenger
            
            Your job is to answer the following questions:
            {query}
            """)


agent= create_sql_agent(
    llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
# 



prompt = PromptTemplate.from_template(template)


def output(text):
    result = agent.run(prompt.format(query=text))
    return result