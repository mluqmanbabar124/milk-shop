
from flask import Blueprint, request, jsonify, current_app
from utils.db import get_db
milk_bp = Blueprint('milk', __name__)

@milk_bp.route('', methods=['GET'])
def list_milk():
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('SELECT * FROM milk_supply ORDER BY date DESC, id DESC')
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)

@milk_bp.route('', methods=['POST'])
def add_milk():
    data = request.get_json() or {}
    date = data.get('date')
    milk_type = data.get('milk_type')
    liters = float(data.get('liters',0))
    rate = float(data.get('rate',0))
    total = liters * rate
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('INSERT INTO milk_supply (date,milk_type,liters,rate,total_amount) VALUES (?,?,?,?,?)',
                (date,milk_type,liters,rate,total))
    conn.commit()
    return jsonify({'message':'created','id':cur.lastrowid}),201

@milk_bp.route('/<int:item_id>', methods=['PUT'])
def update_milk(item_id):
    data = request.get_json() or {}
    date = data.get('date')
    milk_type = data.get('milk_type')
    liters = float(data.get('liters',0))
    rate = float(data.get('rate',0))
    total = liters * rate
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('UPDATE milk_supply SET date=?, milk_type=?, liters=?, rate=?, total_amount=? WHERE id=?',
                (date,milk_type,liters,rate,total,item_id))
    conn.commit()
    return jsonify({'message':'updated'})

@milk_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_milk(item_id):
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('DELETE FROM milk_supply WHERE id=?',(item_id,))
    conn.commit()
    return jsonify({'message':'deleted'})

