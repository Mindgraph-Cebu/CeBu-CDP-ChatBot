
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.sql_database import SQLDatabase

# Define the connection parameters
host = "20.213.35.159"
port = 8123  # ClickHouse native port
user = "default"
password = "Neha12345"
database = "default"

# Construct the connection URI
uri = f"clickhouse://{user}:{password}@{host}:{port}/{database}"

# Initialize SQLDatabase with the connection URI
db = SQLDatabase.from_uri(uri)

# Initialize AzureChatOpenAI
llm = AzureChatOpenAI(model="gpt-35-turbo",
                      openai_api_key="2dd4400d079a4fd49ddd2e864802522a",
                      openai_api_base="https://genai-interns.openai.azure.com/",
                      deployment_name="genai",
                      openai_api_version="2023-07-01-preview",
                      temperature=0)

# Initialize SQLDatabaseToolkit with db and llm
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

template = """
    You are a SQL Analyst querying a database. Below is a description of the columns:

    The column name caseid with the data type object contains the ID of the case
    The column name casetitle with the data type object contains the title of the case
    The column name description with the data type object contains description of the case
    ... (Continue with the rest of the column descriptions)

    Your job is to answer the following questions:
    {query}
"""

agent = create_sql_agent(
    llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

prompt = PromptTemplate.from_template(template)

def output(text):
    result = agent.run(prompt.format(query=text))
    return result
