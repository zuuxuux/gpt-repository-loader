def test_chat_endpoint(client):
    response = client.post("/chat", json={"message": "test"})
    assert response.status_code == 200
    assert "response" in response.json()


def test_chat_invalid_request(client):
    response = client.post("/chat", json={})
    assert response.status_code == 422
