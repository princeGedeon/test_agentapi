import logging

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from contextlib import asynccontextmanager

from core.utils.agent_sql import create_agent_executor



llmqueryrouter = APIRouter()

class QueryRequest(BaseModel):
    question: str

@llmqueryrouter.post("/query-sql", tags=["LLM"])
async def query_sql(req: QueryRequest):
    agent_executor = create_agent_executor()
    try:
        logging.debug("ho")
        result = agent_executor.invoke(req.question)
        logging.info(result)
        return {"question": req.question, "answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
