from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from core.database.init import init_db
from core.routers.exportdata import send_router
from core.routers.importdata import import_router
from core.routers.llmquery import llmqueryrouter
from core.utils.conf_log import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logging.info("Initialisation DB")
    init_db()
    logging.info("Initialisation Modèle ")
    yield
    logging.info("Fermeture")

app = FastAPI(lifespan=lifespan)
app.include_router(import_router)
app.include_router(send_router)
app.include_router(llmqueryrouter)