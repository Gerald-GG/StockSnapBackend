from flask import Blueprint, jsonify, request
from models.stock import StockResource  # Import StockResource from models.stock
from flask_jwt_extended import jwt_required

stocks_routes = Blueprint('stocks_routes', __name__)

# Stock Listing Endpoint
@stocks_routes.route('/stocks', methods=['GET'])
@jwt_required()
def get_stocks():
    try:
        stocks_resource = StockResource()  # Instantiate StockResource
        return stocks_resource.get(), 200  # Call the get method
    except Exception as e:
        return jsonify({"error": "Failed to retrieve stock information."}), 500

# Stock Creation Endpoint
@stocks_routes.route('/stocks', methods=['POST'])
@jwt_required()
def create_stock():
    try:
        stocks_resource = StockResource()  # Instantiate StockResource
        return stocks_resource.post(), 201  # Call the post method
    except Exception as e:
        return jsonify({"error": "Failed to add stock. Please try again later."}), 500
