# tests/test_app.py

import pytest
from noovox.server import app

@pytest.fixture
def client():
    """Create a test client using the Flask application in testing mode."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_users_returns_200(client):
    """Check that GET /api/users returns a 200 and valid JSON."""
    response = client.get('/api/users')
    assert response.status_code == 200, "Expected 200 OK"
    data = response.get_json()
    assert isinstance(data, list), "Expected a JSON array"

def test_non_existent_route_returns_404(client):
    """Ensure a non-existent route returns 404."""
    response = client.get('/api/non-existent')
    assert response.status_code == 404, "Expected 404 Not Found"
