from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

@app.post("/customers")
async def receive_customers(request: Request):
    try:
        data = await request.json()
        logging.info("Données reçues :")
        logging.info(data)
        return {
            "status": "success",
            "message": "Données reçues",
            "nb_customers": len(data.get("customers", [])),
            "nb_purchases": len(data.get("purchases", []))
        }
    except Exception as e:
        logging.error(f"Erreur : {str(e)}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
