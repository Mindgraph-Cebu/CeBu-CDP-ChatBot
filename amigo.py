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
                      temperature=0.7)


template = ("""
            You are a SQL Analyst that is querying a database of a summary of an app called amigo .

            Important note : If the questions are not related to the database simply return "Please ask questions about the database"
                        
            Important note : If the questions are not related to the database simply return "Please ask questions about the database"
                    
            Your job is to answer the following questions:
            {query}
                        
            The output should only only be in string format
            """)
    
uri = "postgresql://postgres:password@localhost:5432/amigo"



db = SQLDatabase.from_uri(uri)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)


agent= create_sql_agent(
        llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True)
    
prompt = PromptTemplate.from_template(template)



    
result = agent.run(prompt.format(query="explain about the database"))

print(result)