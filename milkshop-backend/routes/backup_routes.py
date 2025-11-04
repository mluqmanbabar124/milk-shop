
from flask import Blueprint, send_file, current_app, jsonify
import os

backup_bp = Blueprint('backup', __name__)

@backup_bp.route('/db', methods=['GET'])
def download_db():
    db_path = current_app.config.get('DATABASE','milkshop.db')
    if not os.path.exists(db_path):
        return jsonify({'error':'database not found'}), 404
    # send as attachment
    return send_file(db_path, as_attachment=True, download_name=os.path.basename(db_path))

