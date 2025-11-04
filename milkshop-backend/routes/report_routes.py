
from flask import Blueprint, request, jsonify, current_app, send_file
from utils.db import get_db
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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

@report_bp.route('/monthly-bill', methods=['GET'])
def monthly_bill_pdf():
    """
    Generate a PDF invoice for a single customer.
    Query params: ?customer_id=1&year=2025&month=11
    """
    try:
        customer_id = int(request.args.get('customer_id'))
    except:
        return jsonify({'error':'customer_id required'}), 400
    year = int(request.args.get('year', datetime.now().year))
    month = int(request.args.get('month', datetime.now().month))

    # compute date range
    start = datetime(year,month,1)
    if month==12:
        end = datetime(year+1,1,1)
    else:
        end = datetime(year,month+1,1)
    s = start.strftime('%Y-%m-%d')
    e = (end - timedelta(days=1)).strftime('%Y-%m-%d')

    conn = get_db(current_app.config.get('DATABASE','milkshop.db'))
    cur = conn.cursor()
    cur.execute('SELECT id, name, contact, rate_per_liter FROM monthly_customers WHERE id=?', (customer_id,))
    cust = cur.fetchone()
    if not cust:
        return jsonify({'error':'customer not found'}), 404

    cur.execute('SELECT SUM(liters) as total_liters FROM monthly_supply WHERE customer_id=? AND date BETWEEN ? AND ?',
                (customer_id, s, e))
    total_liters = cur.fetchone()['total_liters'] or 0
    rate = cust['rate_per_liter'] or 0
    total_amount = (total_liters or 0) * rate

    # Generate PDF in-memory using reportlab
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, height - 50, "MilkShop - Monthly Invoice")
    p.setFont("Helvetica", 10)
    p.drawString(40, height - 70, f"Customer: {cust['name']}")
    p.drawString(40, height - 85, f"Contact: {cust['contact'] or ''}")
    p.drawString(40, height - 100, f"Period: {start.strftime('%Y-%m-%d')} to {e}")

    # Table header
    p.setFont("Helvetica-Bold", 11)
    y = height - 140
    p.drawString(40, y, "Description")
    p.drawString(300, y, "Qty (liters)")
    p.drawString(400, y, "Rate")
    p.drawString(480, y, "Amount")

    # Row: milk supply total
    p.setFont("Helvetica", 11)
    y -= 20
    p.drawString(40, y, f"Milk supply for {start.strftime('%B %Y')}")
    p.drawString(300, y, f"{total_liters:.2f}")
    p.drawString(400, y, f"{rate:.2f}")
    p.drawString(480, y, f"{total_amount:.2f}")

    # Summary
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, f"Total: {total_amount:.2f}")

    # Footer / signature
    p.setFont("Helvetica", 10)
    p.drawString(40, 80, "Thank you for your business.")
    p.drawString(40, 60, "Shop Owner Signature: ____________________")

    p.showPage()
    p.save()
    buffer.seek(0)

    filename = f"monthly_bill_customer_{customer_id}_{year}_{month}.pdf"
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

