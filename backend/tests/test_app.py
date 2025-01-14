# tests/test_app.py

import os
import pytest
import mysql.connector
from noovox.server import app

@pytest.fixture
def client():
    """
    Fixture that:
    1. Connects to the DB and truncates the necessary tables.
    2. Configures the Flask test client in TESTING mode.
    3. Yields the Flask test client.
    """
    
    # 1. Truncate tables in the DB
    mysql_host = os.environ.get("MYSQL_HOST", "test-db")
    mysql_user = os.environ.get("MYSQL_USER", "root")
    mysql_password = os.environ.get("MYSQL_PASSWORD", "password")
    mysql_database = os.environ.get("MYSQL_DATABASE", "noovox")

    conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    (f"Connected to database: {os.environ.get('MYSQL_DATABASE', 'noovox')}")
    
    cursor = conn.cursor()
    tables_to_clear = ["chat_messages", "chats", "users", "content_tracking"]

    # Check table contents before truncate
    for table in tables_to_clear:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]

    # Disable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

    for table in tables_to_clear:
        cursor.execute(f"TRUNCATE TABLE {table}")

    # Re-enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    
    # Check table contents after truncate
    for table in tables_to_clear:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
    
    # Commit changes and clean up DB connection
    conn.commit()
    cursor.close()
    conn.close()

    # 2. Configure Flask test client
    app.config['TESTING'] = True
    with app.test_client() as flask_client:
        yield flask_client

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

def test_create_user(client):
    new_user = {
        "username": "testuser",
        "email": "test@example.com"
    }
    response = client.post('/api/users', json=new_user)
    assert response.status_code == 201, "Expected 201 Created"
    data = response.get_json()
    assert data['username'] == new_user['username']
    assert data['email'] == new_user['email']

def test_get_users(client):
    # Create a test user first
    new_user = {
        "username": "testuser",
        "email": "test@example.com"
    }
    client.post('/api/users', json=new_user)
    
    response = client.get('/api/users')
    assert response.status_code == 200, "Expected 200 OK"
    data = response.get_json()
    assert isinstance(data, list), "Expected a list of users"
    assert len(data) > 0, "Expected at least one user"
    assert any(user['username'] == new_user['username'] for user in data)

def test_get_user_by_id(client):
    # Create a user first
    new_user = {
        "username": "testuser",
        "email": "test@example.com"
    }
    create_response = client.post('/api/users', json=new_user)
    created_user = create_response.get_json()
    
    # Get the user by ID
    response = client.get(f'/api/users/{created_user["user_id"]}')
    assert response.status_code == 200, "Expected 200 OK"
    data = response.get_json()
    assert data['user_id'] == created_user['user_id']
    assert data['username'] == new_user['username']

def test_create_chat(client):
    # Create a user first
    new_user = {
        "username": "testuser",
        "email": "test@example.com"
    }
    user_response = client.post('/api/users', json=new_user)
    created_user = user_response.get_json()
    
    # Create a chat for this user
    response = client.post('/api/chats', json={"user_id": created_user['user_id']})
    assert response.status_code == 201, "Expected 201 Created"
    data = response.get_json()
    assert data["user_id"] == created_user['user_id']
    assert "chat_id" in data
    assert "created_at" in data

def test_get_chats(client):
    # Create a user first
    new_user = {
        "username": "testuser",
        "email": "test@example.com"
    }
    user_response = client.post('/api/users', json=new_user)
    created_user = user_response.get_json()
    
    # Create a chat
    chat_response = client.post('/api/chats', json={"user_id": created_user['user_id']})
    created_chat = chat_response.get_json()
    
    # Get all chats
    response = client.get('/api/chats')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(chat['chat_id'] == created_chat['chat_id'] for chat in data)

def test_send_chat_message(client):
    # Create a user first
    new_user = {
        "username": "testuser",
        "email": "test@example.com"
    }
    user_response = client.post('/api/users', json=new_user)
    created_user = user_response.get_json()
    
    # Create a chat
    chat_response = client.post('/api/chats', json={"user_id": created_user['user_id']})
    created_chat = chat_response.get_json()
    
    # Send a message
    message_data = {
        "user_id": created_user['user_id'],
        "sender_type": "user",
        "message_text": "Hello from a test!"
    }
    response = client.post(f'/api/chats/{created_chat["chat_id"]}/messages', json=message_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['sender_type'] == "user"
    assert data['message_text'] == "Hello from a test!"
    assert data['user_id'] == created_user['user_id']
    assert data['chat_id'] == created_chat['chat_id']

def test_get_chat_messages(client):
    # Create a user first
    new_user = {
        "username": "testuser",
        "email": "test@example.com"
    }
    user_response = client.post('/api/users', json=new_user)
    created_user = user_response.get_json()
    
    # Create a chat
    chat_response = client.post('/api/chats', json={"user_id": created_user['user_id']})
    created_chat = chat_response.get_json()
    
    # Send a message
    message_data = {
        "user_id": created_user['user_id'],
        "sender_type": "user",
        "message_text": "Test message"
    }
    client.post(f'/api/chats/{created_chat["chat_id"]}/messages', json=message_data)
    
    # Get all messages
    response = client.get(f'/api/chats/{created_chat["chat_id"]}/messages')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['message_text'] == "Test message"