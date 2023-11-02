from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
import duckdb
import pandas as pd
from langchain.schema import HumanMessage

llm = AzureChatOpenAI(model="gpt-35-turbo",
                      openai_api_key="2dd4400d079a4fd49ddd2e864802522a",
                      openai_api_base="https://genai-interns.openai.azure.com/",
                      deployment_name="genai",
                      openai_api_version="2023-07-01-preview",
                      temperature=0.7,)


res = llm([HumanMessage(content="hi")])
print(res)