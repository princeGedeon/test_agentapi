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

        # Vérifications
        missing_customers = [col for col in REQUIRED_CUSTOMER_COLUMNS if col not in customers_df.columns]
        missing_purchases = [col for col in REQUIRED_PURCHASE_COLUMNS if col not in purchases_df.columns]

        if missing_customers:
            raise HTTPException(status_code=400, detail=f"Colonnes manquantes dans customers.csv : {missing_customers}")
        if missing_purchases:
            raise HTTPException(status_code=400, detail=f"Colonnes manquantes dans purchases.csv : {missing_purchases}")
        # Filtrer les doublons d'ID déjà dans customers
        existing_customer_ids = pd.read_sql_query("SELECT customer_id FROM customers", conn)["customer_id"].tolist()
        new_customers_df = customers_df[~customers_df["customer_id"].isin(existing_customer_ids)]
        # Idem pour purchases
        existing_purchase_ids = pd.read_sql_query("SELECT purchase_identifier FROM purchases", conn)["purchase_identifier"].tolist()
        new_purchases_df = purchases_df[~purchases_df["purchase_identifier"].isin(existing_purchase_ids)]
       # enelver les elements qui ont plus de 4 valeurs manquantes
        new_purchases_df = new_purchases_df.dropna(thresh=new_purchases_df.shape[1] - 4)
        new_customers_df = new_customers_df.dropna(thresh=new_customers_df.shape[1] - 4)
        # import avec pandas
        new_customers_df.to_sql("customers", conn, if_exists="append", index=False)
        new_purchases_df.to_sql("purchases", conn, if_exists="append", index=False)
        conn.commit()
        conn.close()
        return {
                "rows_inserted": {
                    "customers": len(new_customers_df),
                    "purchases": len(new_purchases_df)
                },
                "rows_ignored": {
                    "customers": len(customers_df) - len(new_customers_df),
                    "purchases": len(purchases_df) - len(new_purchases_df)
                }
            }

    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Erreur de parsing CSV. Vérifie le format des fichiers.")
    except sqlite3.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inconnue : {str(e)}")
