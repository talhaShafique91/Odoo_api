from flask import Flask, request, jsonify
from app.odoo_client import OdooClient
from app.order_processor import OrderProcessor

app = Flask(__name__)

@app.route('/process_orders', methods=['POST'])
def process_orders():
    try:
        data = request.json
        odoo_client = OdooClient(data['url'], data['db'], data['username'], data['password'])
        processor = OrderProcessor(odoo_client, data['csv_path'])
        processor.process_orders()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
