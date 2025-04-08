import io

def test_import_csv_success(client):

    customers_csv = """customer_id,title,lastname,firstname,postal_code,city,email
1,2,Norris,Chuck,83600,Fréjus,chuck@norris.com
2,1,Galante,Marie,75001,Paris,marie@galante.fr
"""

    purchases_csv = f"""purchase_identifier,product_id,quantity,price,currency,date,customer_id
1001,ABC123,2,19.99,EUR,2024-01-01,1
1002,XYZ789,1,9.99,EUR,2024-01-02,2
"""
    response = client.post(
        "/import-csv",
        files={
            "customers_file": ("customers.csv", io.BytesIO(customers_csv.encode("utf-8")), "text/csv"),
            "purchases_file": ("purchases.csv", io.BytesIO(purchases_csv.encode("utf-8")), "text/csv"),
        }
    )
    print(response.json())
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["rows_inserted"]["customers"] == 2
    assert data["rows_inserted"]["purchases"] == 2


import io


def test_import_csv_conflict(client):
    customers_csv = """customer_id,title,lastname,firstname,postal_code,city,email
3,2,Norris,Chuck,83600,Fréjus,chuck@norris.com
3,1,Galante,Marie,75001,Paris,marie@galante.fr
"""

    purchases_csv = f"""purchase_identifier,product_id,quantity,price,currency,date,customer_id
1008,ABC123,2,19.99,EUR,2024-01-01,1
1008,XYZ789,1,9.99,EUR,2024-01-02,2
"""
    response = client.post(
        "/import-csv",
        files={
            "customers_file": ("customers.csv", io.BytesIO(customers_csv.encode("utf-8")), "text/csv"),
            "purchases_file": ("purchases.csv", io.BytesIO(purchases_csv.encode("utf-8")), "text/csv"),
        }
    )


    data = response.json()
    assert data["detail"] == "Erreur SQLite : UNIQUE constraint failed: customers.customer_id"

