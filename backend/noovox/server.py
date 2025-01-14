import argparse
import os
import sys

import dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector

from noovox.core import DummyProvider, OpenAIProvider

assert dotenv.load_dotenv

llm = None

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)



app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": [
                        "http://localhost:5173",  # dev
                        "http://localhost:3000",  # "prod"
                    ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'noovox')

swagger_url = '/swagger'
swagger_ui_blueprint = get_swaggerui_blueprint(
    swagger_url,
    '/static/swagger.json',
    config={'app_name': "Noovox API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=swagger_url)


def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )


@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Insert the user
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", 
                      (data['username'], data['email']))
        
        # Get the new user's ID
        new_user_id = cursor.lastrowid
        
        # Fetch the complete new user record
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (new_user_id,))
        new_user = cursor.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify(new_user), 201

    except mysql.connector.Error as db_err:
        print(f"MySQL Error: {db_err}")
        return jsonify({"error": "Database error", "details": str(db_err)}), 500
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({"error": "Unexpected error occurred.", "details": str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = %s, email = %s WHERE user_id = %s",
                   (data['username'], data['email'], user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(data)


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204


@app.route('/api/chats', methods=['GET'])
def get_chats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chats")
    chats = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(chats)


@app.route('/api/chats', methods=['POST'])
def create_chat():
    """
    Create a new chat. 
    - The database automatically generates chat_id (AUTO_INCREMENT) and created_at (DEFAULT CURRENT_TIMESTAMP).
    - The frontend should only send user_id in the JSON body, e.g.:
        {
            "user_id": 123
        }
    """
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    # Make sure 'user_id' is present
    user_id = data.get('user_id')
    if user_id is None:
        return jsonify({"error": "Missing required field 'user_id'"}), 400

    try:
        conn = get_db_connection()
        # Use dictionary cursor so we can return data as a dict
        cursor = conn.cursor(dictionary=True)
        
        # Insert only user_id; MySQL will auto-generate chat_id and created_at
        insert_query = "INSERT INTO chats (user_id) VALUES (%s)"
        cursor.execute(insert_query, (user_id,))
        
        # Grab the auto-generated ID
        new_chat_id = cursor.lastrowid

        conn.commit()

        # Fetch the newly created record so we can return it
        cursor.execute("SELECT chat_id, user_id, created_at FROM chats WHERE chat_id = %s", (new_chat_id,))
        new_chat = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Return the newly created chat (including auto-generated fields)
        return jsonify(new_chat), 201

    except mysql.connector.Error as db_err:
        # Handle database-related errors (e.g., foreign key constraint fails if user_id doesn't exist)
        print(f"MySQL Error: {db_err}")
        return jsonify({"error": "Database error", "details": str(db_err)}), 500
    except Exception as e:
        # Handle any other unexpected exceptions
        print(f"Unexpected Error: {e}")
        return jsonify({"error": "Unexpected error occurred.", "details": str(e)}), 500



@app.route('/api/chats/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chats WHERE chat_id = %s", (chat_id,))
    chat = cursor.fetchone()
    cursor.close()
    conn.close()
    if chat:
        return jsonify(chat)
    return jsonify({'error': 'Chat not found'}), 404


@app.route('/api/chats/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats WHERE chat_id = %s", (chat_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204


@app.route('/api/chats/<int:chat_id>/messages', methods=['GET'])
def get_chat_messages(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chat_messages WHERE chat_id = %s", (chat_id,))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(messages)


@app.route('/api/chats/<int:chat_id>/messages', methods=['POST'])
def send_chat_message(chat_id):
    """
    Create a new chat message in a specific chat. If the sender_type is 'user',
    automatically generate an assistant response.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    # Validate required fields
    user_id = data.get('user_id')
    sender_type = data.get('sender_type')
    message_text = data.get('message_text')

    missing_fields = []
    if user_id is None:
        missing_fields.append("user_id")
    if sender_type is None:
        missing_fields.append("sender_type")
    if message_text is None:
        missing_fields.append("message_text")
    if missing_fields:
        return jsonify({"error": f"Missing required field(s): {', '.join(missing_fields)}"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Insert the user's message
        insert_query = """
            INSERT INTO chat_messages (chat_id, user_id, sender_type, message_text) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (chat_id, user_id, sender_type, message_text))
        user_message_id = cursor.lastrowid
        conn.commit()

        # If this is a user message, generate and store an assistant response
        response_message = None
        if sender_type == 'user':
            # Generate assistant response using the DummyProvider
            assistant_response = llm(message_text)
            
            # Store the assistant's response
            cursor.execute(insert_query, (chat_id, user_id, 'assistant', assistant_response))
            assistant_message_id = cursor.lastrowid
            conn.commit()
            
            # Fetch both messages
            cursor.execute(
                "SELECT * FROM chat_messages WHERE message_id IN (%s, %s)", 
                (user_message_id, assistant_message_id)
            )
            response_message = cursor.fetchall()
        else:
            # If it's not a user message, just fetch the single message
            cursor.execute(
                "SELECT * FROM chat_messages WHERE message_id = %s", 
                (user_message_id,)
            )
            response_message = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(response_message), 201

    except mysql.connector.Error as db_err:
        print(f"MySQL Error: {db_err}")
        return jsonify({"error": "Database error", "details": str(db_err)}), 500
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({"error": "Unexpected error occurred.", "details": str(e)}), 500



@app.route('/api/content_tracking', methods=['GET'])
def get_content_tracking():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM content_tracking")
    tracking_records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tracking_records)


@app.route('/api/content_tracking', methods=['POST'])
def track_content():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO content_tracking (user_id, content_type, content_id) VALUES (%s, %s, %s)",
                   (data['user_id'], data['content_type'], data['content_id']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(data), 201


@app.route("/")
def home():
    return "Noovox Backend is Running!"

def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments, e.g.:
      python server.py --deploy
    """
    parser = argparse.ArgumentParser(description="Noovox server runner")
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Use OpenAIProvider for LLM (production mode). If not provided, defaults to DummyProvider (dev mode)."
    )
    return parser.parse_args()


def main():
    # 1) Parse CLI args
    args = parse_args()

    # 2) Decide which LLM provider to use
    global llm
    if args.deploy:
        print("Using OpenAIProvider for LLM (deploy mode)")
        llm = OpenAIProvider(
            api_key=os.getenv("OPEN_AI_KEY"),  # Ensure this is set in your environment
            model="gpt-4",
            temperature=0.2
        )
        debug_mode = False
    else:
        print("Using DummyProvider for LLM (dev mode)")
        llm = DummyProvider()
        debug_mode = True

    # 3) Run the app
    print("Swagger UI URL: http://localhost:5000/swagger")
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
