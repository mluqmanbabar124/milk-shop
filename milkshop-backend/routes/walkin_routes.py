
from flask import Blueprint, request, jsonify, current_app
from utils.db import get_db
walkin_bp = Blueprint('walkin', __name__)

@walkin_bp.route('', methods=['GET'])
def list_walkin():
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('SELECT * FROM walkin_sales ORDER BY date DESC, id DESC')
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)

@walkin_bp.route('', methods=['POST'])
def add_walkin():
    data = request.get_json() or {}
    date = data.get('date')
    customer_name = data.get('customer_name') or ''
    liters = float(data.get('liters',0))
    rate = float(data.get('rate',0))
    total = liters * rate
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('INSERT INTO walkin_sales (date,customer_name,liters,rate,total_amount) VALUES (?,?,?,?,?)',
                (date,customer_name,liters,rate,total))
    conn.commit()
    return jsonify({'message':'created','id':cur.lastrowid}),201

@walkin_bp.route('/<int:item_id>', methods=['PUT'])
def update_walkin(item_id):
    data = request.get_json() or {}
    date = data.get('date')
    customer_name = data.get('customer_name') or ''
    liters = float(data.get('liters',0))
    rate = float(data.get('rate',0))
    total = liters * rate
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('UPDATE walkin_sales SET date=?, customer_name=?, liters=?, rate=?, total_amount=? WHERE id=?',
                (date,customer_name,liters,rate,total,item_id))
    conn.commit()
    return jsonify({'message':'updated'})

@walkin_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_walkin(item_id):
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('DELETE FROM walkin_sales WHERE id=?',(item_id,))
    conn.commit()
    return jsonify({'message':'deleted'})

