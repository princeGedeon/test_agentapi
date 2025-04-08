def test_send_customers_to_external_api(client):
    response = client.post("/send-customers?api_url=http:\\empty.com")

    assert response.status_code == 500



