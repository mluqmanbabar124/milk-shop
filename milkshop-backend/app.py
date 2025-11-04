from flask import Flask, jsonify
from utils import db as db_utils
from routes.auth_routes import auth_bp
from routes.milk_routes import milk_bp
from routes.walkin_routes import walkin_bp
from routes.monthly_routes import monthly_bp
from routes.report_routes import report_bp
from routes.backup_routes import backup_bp
import argparse
from flask_cors import CORS
from flasgger import Swagger


def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = 'milkshop.db'

    # ✅ Initialize Swagger
    Swagger(app, template={
        "info": {
            "title": "Milk Shop API",
            "description": "Offline milk shop management API",
            "version": "1.0.0"
        },
        "schemes": ["http"],
    })

    # ✅ Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(milk_bp, url_prefix='/api/milk')
    app.register_blueprint(walkin_bp, url_prefix='/api/walkin')
    app.register_blueprint(monthly_bp, url_prefix='/api/customers')
    app.register_blueprint(report_bp, url_prefix='/api/reports')
    app.register_blueprint(backup_bp, url_prefix='/api/backup')

    @app.route('/')
    def index():
        return jsonify({'message': 'MilkShop backend running'})

    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--init-db', action='store_true', help='Initialize the database and create default admin')
    args = parser.parse_args()

    if args.init_db:
        db_utils.init_db('milkshop.db', init_admin=True)
        print('Database initialized with default admin (username: admin, password: 1234)')

    app = create_app()
    # ✅ Enable CORS so Angular (localhost:4200) can call Flask
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db_utils.init_db('milkshop.db', init_admin=False)
    app.run(host='127.0.0.1', port=5000, debug=True)
