import logging
from fastapi import FastAPI, HTTPException, APIRouter, Request
from pydantic import BaseModel
from contextlib import asynccontextmanager

from core.utils.agent_sql import create_agent_executor

llmqueryrouter = APIRouter()

# Classe de la requête
class QueryRequest(BaseModel):
    question: str

# Stockage du modèle dans l'état de l'application
@llmqueryrouter.post("/query-sql", tags=["LLM"])
async def query_sql(req: QueryRequest, request: Request):
    agent_executor = request.app.state.agent_executor
    try:
        logging.debug("ho")
        result = agent_executor.invoke(req.question)
        logging.info(result)
        return {"question": req.question, "answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






