from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from flask import Flask, jsonify, request

# ClickHouse connection parameters
host_clickhouse = "20.213.35.159"
port_clickhouse = 8123
user_clickhouse = "default"
password_clickhouse = "Neha12345"
database_clickhouse = "default"
uri_clickhouse = f"clickhouse://{user_clickhouse}:{password_clickhouse}@{host_clickhouse}:{port_clickhouse}/{database_clickhouse}"

# SQLite (Passenger database) connection parameters
uri_passenger = "sqlite:///data.db"

# Initialize AzureChatOpenAI
llm = AzureChatOpenAI(
    model="gpt-35-turbo",
    openai_api_key="2dd4400d079a4fd49ddd2e864802522a",
    openai_api_base="https://genai-interns.openai.azure.com/",
    deployment_name="genai",
    openai_api_version="2023-07-01-preview",
    temperature=0
)

# Initialize SQLDatabaseToolkit for ClickHouse
db_clickhouse = SQLDatabase.from_uri(uri_clickhouse)
toolkit_clickhouse = SQLDatabaseToolkit(db=db_clickhouse, llm=llm)

# Initialize SQLDatabaseToolkit for SQLite (Passenger database)
db_passenger = SQLDatabase.from_uri(uri_passenger)
toolkit_passenger = SQLDatabaseToolkit(db=db_passenger, llm=llm)

# Prompt template for both databases
template_clickhouse = """
    You are a SQL Analyst querying a ClickHouse database. Below is a description of the columns:

    The column name caseid with the data type object contains the ID of the case
    The column name casetitle with the data type object contains the title of the case
    The column name description with the data type object contains the description of the case
    ... (Continue with the rest of the ClickHouse column descriptions)

    Your job is to answer the following questions:
    {query}
"""

# Template for Passenger Database
template_passenger = """
    You are a SQL Analyst querying a Passenger Database. Below is a description of the columns:

    The column name Passenger_name with the data type object contains the names of the passengers
    The column name Arrival_station with the data type object contains the arrival station of the passenger
    The column name Departure_station with the data type object contains the departure station of the passenger
    ... (Continue with the rest of the Passenger column descriptions)

    Your job is to answer the following questions:
    {query}
"""

# Create agents for both databases
agent_clickhouse = create_sql_agent(
    llm,
    toolkit=toolkit_clickhouse,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

agent_passenger = create_sql_agent(
    llm,
    toolkit=toolkit_passenger,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

def get_response_clickhouse(query):
    response_clickhouse = agent_clickhouse.run(template_clickhouse.format(query=query))
    return response_clickhouse

def get_response_passenger(query):
    response_passenger = agent_passenger.run(template_passenger.format(query=query))
    return response_passenger
