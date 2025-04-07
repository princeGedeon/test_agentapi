import logging
import os
import sqlite3
import pandas as pd
import requests
from fastapi import APIRouter, HTTPException, Query
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from core.utils.tools import fetch_data_from_sqlite

send_router = APIRouter()
DEFAULT_API_URL = os.getenv("EXTERNAL_API_URL", "https://mockapi.example.com/v1/customers")


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type(requests.RequestException),
)
def send_to_api(payload: dict, url: str):
    response = requests.post(url, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()



@send_router.post("/send-customers", summary="Envoi vers API externe avec résilience", tags=["Send"])
def send_customers(api_url: str = Query(default=None, description="URL API externe (optionnel)")):
    try:
        db_path = os.getenv("DATABASE_PATH", "./data/flight.db")
        if not os.path.exists(db_path):
            raise HTTPException(status_code=400, detail="Base de données introuvable.")

        customers, purchases = fetch_data_from_sqlite(db_path)

        payload = {
            "customers": customers,
            "purchases": purchases
        }

        logging.info(f"Send customers via API: {api_url}")

        url_to_use = DEFAULT_API_URL if api_url is None else api_url
        response = send_to_api(payload, url_to_use)

        return {

            "external_url": url_to_use,
            "external_response": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'envoi : {str(e)}")
