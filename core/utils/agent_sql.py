import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import AgentType
from langchain_ollama import OllamaLLM

def load_database():
    db_path = os.getenv("DATABASE_PATH", "./data/flight.db")
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    print("Base chargée :", db.dialect)
    return db

def load_llm():
    model_name = os.getenv("OLLAMA_MODEL", "phi3")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    llm = OllamaLLM(
        model=model_name,
        base_url=base_url,
        temperature=0.1,
    )


    print(f"Modèle chargé : {model_name} avec Ollama")
    return llm

def create_agent_executor():
    db = load_database()
    llm = load_llm()

    agent = create_sql_agent(
        llm=llm,

        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent
