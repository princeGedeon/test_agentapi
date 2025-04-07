import sqlite3

import pandas as pd
from fastapi import UploadFile


def detect_separator(upload_file: UploadFile) -> str:
    """Détecte si le CSV utilise ',' ou ';'r"""
    first_line = upload_file.file.readline().decode("utf-8")
    upload_file.file.seek(0)
    return ";" if ";" in first_line else ","

def fetch_data_from_sqlite(db_path: str):
    conn = sqlite3.connect(db_path)
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    purchases_df = pd.read_sql_query("SELECT * FROM purchases", conn)
    conn.close()
    return customers_df.to_dict(orient="records"), purchases_df.to_dict(orient="records")