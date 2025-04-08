from unittest.mock import Mock, patch


def test_send_customers_to_external_api(client):
    response = client.post("/send-customers?api_url=http:\\empty.com")

    assert response.status_code == 500




def test_send_customers_success(client):
    fake_customers = [{"id": 1, "name": "John"}]
    fake_purchases = [{"id": 1, "customer_id": 1, "item": "Laptop", "amount": 1299.99}]

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}

    with patch("core.routers.exportdata.fetch_data_from_sqlite", return_value=(fake_customers, fake_purchases)), \
            patch("core.routers.exportdata.requests.post", return_value=mock_response):
        response = client.post("/send-customers?api_url=http://fake-api.com")

        assert response.status_code == 200
        json_data = response.json()

        assert json_data["external_url"] == "http://fake-api.com"
        assert json_data["external_response"] == {"status": "ok"}
