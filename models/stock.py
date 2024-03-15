from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db  # Import db from models package

class StockResource(Resource):
    @staticmethod
    @jwt_required()
    def get(Stock):
        try:
            stocks = Stock.query.all()
            stock_data = []
            for stock in stocks:
                stock_info = {
                    "id": stock.id,
                    "name": stock.name,
                    "quantity": stock.quantity,
                    "company": stock.company,
                    "date_added": stock.date_added
                }
                stock_data.append(stock_info)
            return jsonify(stock_data), 200
        except Exception as e:
            return {"error": "Failed to retrieve stock information."}, 500

    @staticmethod
    @jwt_required()
    def post(Stock):
        try:
            data = request.get_json()
            name = data.get('name')
            quantity = data.get('quantity')
            company = data.get('company')

            if not name or not quantity or not company:
                return {"error": "Name, quantity, and company are required."}, 400

            new_stock = Stock(name=name, quantity=quantity, company=company)
            db.session.add(new_stock)
            db.session.commit()
            return {"message": "Stock added successfully."}, 201
        except Exception as e:
            return {"error": "Failed to add stock. Please try again later."}, 500

    @staticmethod
    @jwt_required()
    def put(Stock, stock_id):
        try:
            data = request.get_json()
            name = data.get('name')
            quantity = data.get('quantity')
            company = data.get('company')

            stock = Stock.query.filter_by(id=stock_id).first()
            if not stock:
                return {"error": "Stock not found."}, 404

            # Update stock information
            stock.name = name
            stock.quantity = quantity
            stock.company = company
            db.session.commit()
            return {"message": "Stock updated successfully."}, 200
        except Exception as e:
            return {"error": "Failed to update stock information."}, 500

    @staticmethod
    @jwt_required()
    def delete(Stock, stock_id):
        try:
            stock = Stock.query.filter_by(id=stock_id).first()
            if not stock:
                return {"error": "Stock not found."}, 404

            db.session.delete(stock)
            db.session.commit()
            return {"message": "Stock deleted successfully."}, 200
        except Exception as e:
            return {"error": "Failed to delete stock."}, 500
