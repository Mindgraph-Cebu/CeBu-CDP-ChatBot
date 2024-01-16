
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.sql_database import SQLDatabase

# Define the connection parameters
snowflake_account = 'wzadpnd-vh55113'
snowflake_user = 'GENAI'
snowflake_password = 'Genai2024'
snowflake_database = 'CUS360'
snowflake_schema = 'PUBLIC'

# Build the Snowflake connection URI
uri = f'snowflake://{snowflake_user}:{snowflake_password}@{snowflake_account}/{snowflake_database}/{snowflake_schema}'


# Initialize SQLDatabase with the connection URI
db = SQLDatabase.from_uri(uri)

# Initialize AzureChatOpenAI
llm = AzureChatOpenAI(model="genai",
                      api_key="2dd4400d079a4fd49ddd2e864802522a",
                      openai_api_base="https://genai-interns.openai.azure.com/",
                      deployment_name="genai",
                      openai_api_version="2023-07-01-preview",
                      temperature=0)

# Initialize SQLDatabaseToolkit with db and llm
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

template = """
    You are a SQL Analyst querying a database. Below is a description of the columns:

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

