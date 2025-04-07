from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from contextlib import asynccontextmanager

from core.utils.agent_sql import create_agent_executor

agent_executor = None


@asynccontextmanager
async def lifespan(app):
    global agent_executor
    print("Initialisation agent IA ")
    agent_executor = create_agent_executor()
    yield
    print("Fin agent IA ")

llmqueryrouter = APIRouter(lifespan=lifespan)

class QueryRequest(BaseModel):
    question: str

@llmqueryrouter.post("/query-sql", tags=["LLM"])
async def query_sql(req: QueryRequest):
    global agent_executor
    try:
        result = agent_executor.run(req.question)
        return {"question": req.question, "answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
