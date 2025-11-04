
from flask import Blueprint, request, jsonify, current_app
from utils.db import get_db
from datetime import datetime, timedelta
report_bp = Blueprint('reports', __name__)

@report_bp.route('/daily', methods=['GET'])
def daily_report():
    qdate = request.args.get('date')
    if not qdate:
        qdate = datetime.now().strftime('%Y-%m-%d')
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('SELECT SUM(liters) as total_liters, SUM(total_amount) as total_cost FROM milk_supply WHERE date=?',(qdate,))
    milk = dict(cur.fetchone())
    cur.execute('SELECT SUM(liters) as total_liters, SUM(total_amount) as total_amount FROM walkin_sales WHERE date=?',(qdate,))
    walkin = dict(cur.fetchone())
    cur.execute('SELECT SUM(liters) as total_liters FROM monthly_supply WHERE date=?',(qdate,))
    monthly = dict(cur.fetchone())
    return jsonify({'date':qdate,'milk_received':milk,'walkin_sales':walkin,'monthly_supply':monthly})

@report_bp.route('/monthly', methods=['GET'])
def monthly_report():
    year = int(request.args.get('year', datetime.now().year))
    month = int(request.args.get('month', datetime.now().month))
    start = datetime(year,month,1)
    if month==12:
        end = datetime(year+1,1,1)
    else:
        end = datetime(year,month+1,1)
    s = start.strftime('%Y-%m-%d')
    e = (end - timedelta(days=1)).strftime('%Y-%m-%d')
    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('SELECT id, name, rate_per_liter FROM monthly_customers WHERE active=1')
    customers = []
    for r in cur.fetchall():
        cid = r['id']
        name = r['name']
        rate = r['rate_per_liter'] or 0
        cur2 = conn.cursor()
        cur2.execute('SELECT SUM(liters) as total_liters FROM monthly_supply WHERE customer_id=? AND date BETWEEN ? AND ?',(cid,s,e))
        tot = cur2.fetchone()['total_liters'] or 0
        bill = tot * rate
        customers.append({'id':cid,'name':name,'total_liters':tot,'rate_per_liter':rate,'bill':bill})
    return jsonify({'year':year,'month':month,'customers':customers})

