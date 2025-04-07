import os
import sqlite3
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File
from core.utils.constants import REQUIRED_CUSTOMER_COLUMNS, REQUIRED_PURCHASE_COLUMNS
from core.utils.tools import detect_separator

import_router = APIRouter()


@import_router.post("/import-csv", summary="Uploader deux fichiers CSV", tags=["Import"])
async def import_csv(
    customers_file: UploadFile = File(..., description="CSV des customers"),
    purchases_file: UploadFile = File(..., description="CSV des purchases"),
):
    try:
        # Check extensions
        for f in [customers_file, purchases_file]:
            if not f.filename.endswith(".csv"):
                raise HTTPException(status_code=400, detail=f"Le fichier {f.filename} n'est pas un CSV.")


        db_path = os.getenv("DATABASE_PATH", "./data/flight.db")
        conn = sqlite3.connect(db_path)
        # Vérifier le séparateur
        sep_customers = detect_separator(customers_file)
        sep_purchases = detect_separator(purchases_file)

        # Load csv avec pandas
        customers_df = pd.read_csv(customers_file.file,sep=sep_customers)
        purchases_df = pd.read_csv(purchases_file.file,sep=sep_purchases   )
        print(customers_df.head())
        print(purchases_df.head())

        # Vérifications
        missing_customers = [col for col in REQUIRED_CUSTOMER_COLUMNS if col not in customers_df.columns]
        missing_purchases = [col for col in REQUIRED_PURCHASE_COLUMNS if col not in purchases_df.columns]

        if missing_customers:
            raise HTTPException(status_code=400, detail=f"Colonnes manquantes dans customers.csv : {missing_customers}")
        if missing_purchases:
            raise HTTPException(status_code=400, detail=f"Colonnes manquantes dans purchases.csv : {missing_purchases}")

        # 💾 Importer dans la DB (append)
        customers_df.to_sql("customers", conn, if_exists="append", index=False)
        purchases_df.to_sql("purchases", conn, if_exists="append", index=False)

        nb_customers = len(customers_df)
        nb_purchases = len(purchases_df)

        conn.commit()
        conn.close()

        return {
           "rows_inserted": {
                "customers": nb_customers,
                "purchases": nb_purchases
            }
        }

    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Erreur de parsing CSV. Vérifie le format des fichiers.")
    except sqlite3.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue : {str(e)}")
