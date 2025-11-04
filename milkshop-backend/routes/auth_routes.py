
from flask import Blueprint, request, jsonify, current_app
from utils.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
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

