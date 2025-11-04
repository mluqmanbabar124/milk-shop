
from flask import Blueprint, request, jsonify, current_app
from utils.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'example': {
                    "username": "admin",
                    "password": "1234"
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Response example', 'examples': {
            'application/json': {
                "success": True,
                "message": "User created successfully",
                "data": None
            }
        }}
    }
})
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    pw_hash = generate_password_hash(password)
    try:
        cur.execute('INSERT INTO users (username, password_hash) VALUES (?,?)', (username, pw_hash))
        conn.commit()
        return jsonify({'message':'user created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])

def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    if not row:
        return jsonify({'error':'invalid credentials'}), 401
    if not check_password_hash(row['password_hash'], password):
        return jsonify({'error':'invalid credentials'}), 401
    return jsonify({'message':'ok','user':{'id':row['id'],'username':row['username']}})

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """
    JSON: { "username": "...", "old_password": "...", "new_password": "..." }
    """
    data = request.get_json() or {}
    username = data.get('username')
    old_pw = data.get('old_password')
    new_pw = data.get('new_password')
    if not username or not old_pw or not new_pw:
        return jsonify({'error':'username, old_password and new_password required'}), 400
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    if not row:
        return jsonify({'error':'user not found'}), 404
    if not check_password_hash(row['password_hash'], old_pw):
        return jsonify({'error':'invalid current password'}), 401
    new_hash = generate_password_hash(new_pw)
    cur.execute('UPDATE users SET password_hash=? WHERE username=?', (new_hash, username))
    conn.commit()
    return jsonify({'message':'password changed'})

