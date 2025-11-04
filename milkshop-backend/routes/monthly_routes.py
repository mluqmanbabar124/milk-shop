
from flask import Blueprint, request, jsonify, current_app
from utils.db import get_db
monthly_bp = Blueprint('monthly', __name__)

@monthly_bp.route('', methods=['GET'])
def list_customers():
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('SELECT * FROM monthly_customers ORDER BY id DESC')
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)

@monthly_bp.route('', methods=['POST'])
def add_customer():
    data = request.get_json() or {}
    name = data.get('name')
    contact = data.get('contact') or ''
    milk_type = data.get('milk_type') or ''
    rate = float(data.get('rate_per_liter',0))
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('INSERT INTO monthly_customers (name,contact,milk_type,rate_per_liter,active) VALUES (?,?,?,?,1)',
                (name,contact,milk_type,rate))
    conn.commit()
    return jsonify({'message':'created','id':cur.lastrowid}),201

@monthly_bp.route('/<int:cust_id>', methods=['PUT'])
def update_customer(cust_id):
    data = request.get_json() or {}
    name = data.get('name')
    contact = data.get('contact') or ''
    milk_type = data.get('milk_type') or ''
    rate = float(data.get('rate_per_liter',0))
    active = int(data.get('active',1))
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('UPDATE monthly_customers SET name=?, contact=?, milk_type=?, rate_per_liter=?, active=? WHERE id=?',
                (name,contact,milk_type,rate,active,cust_id))
    conn.commit()
    return jsonify({'message':'updated'})

@monthly_bp.route('/<int:cust_id>', methods=['DELETE'])
def delete_customer(cust_id):
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('DELETE FROM monthly_customers WHERE id=?',(cust_id,))
    conn.commit()
    return jsonify({'message':'deleted'})

# Monthly supply entries
@monthly_bp.route('/supply', methods=['GET'])
def list_monthly_supply():
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('SELECT ms.*, mc.name as customer_name FROM monthly_supply ms LEFT JOIN monthly_customers mc ON ms.customer_id=mc.id ORDER BY ms.date DESC')
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)

@monthly_bp.route('/supply', methods=['POST'])
def add_monthly_supply():
    data = request.get_json() or {}
    customer_id = int(data.get('customer_id'))
    date = data.get('date')
    liters = float(data.get('liters',0))
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('INSERT INTO monthly_supply (customer_id,date,liters) VALUES (?,?,?)',(customer_id,date,liters))
    conn.commit()
    return jsonify({'message':'created','id':cur.lastrowid}),201

@monthly_bp.route('/supply/<int:item_id>', methods=['DELETE'])
def delete_monthly_supply(item_id):
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('DELETE FROM monthly_supply WHERE id=?',(item_id,))
    conn.commit()
    return jsonify({'message':'deleted'})

