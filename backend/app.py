from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import json
import os

app = Flask(__name__)
CORS(app)

# Custom JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

app.json_encoder = JSONEncoder

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(mongo_uri)
db = client.mayabazar

# Collections
products_col = db.products
orders_col = db.orders

# Sample products
SAMPLE_PRODUCTS = [
    {"id": 1, "name": "Silk Kurta", "price": 1299, "category": "dress", "image_url": "https://images.pexels.com/photos/6311383/pexels-photo-6311383.jpeg"},
    {"id": 2, "name": "Casual Shirt", "price": 899, "category": "dress", "image_url": "https://images.pexels.com/photos/842811/pexels-photo-842811.jpeg"},
    {"id": 3, "name": "Kids Cycle", "price": 3999, "category": "cycle", "image_url": "https://images.pexels.com/photos/296735/pexels-photo-296735.jpeg"},
    {"id": 4, "name": "Gear Cycle", "price": 8499, "category": "cycle", "image_url": "https://images.pexels.com/photos/276517/pexels-photo-276517.jpeg"},
    {"id": 5, "name": "Girls Sneakers", "price": 999, "category": "shoes", "image_url": "https://images.pexels.com/photos/4210853/pexels-photo-4210853.jpeg"},
    {"id": 6, "name": "Boys Running", "price": 1199, "category": "shoes", "image_url": "https://images.pexels.com/photos/7005601/pexels-photo-7005601.jpeg"},
    {"id": 7, "name": "Hawai Slipper", "price": 199, "category": "slipper", "image_url": "https://images.pexels.com/photos/1202911/pexels-photo-1202911.jpeg"},
    {"id": 8, "name": "Masala Tea", "price": 25, "category": "tea", "image_url": "https://images.pexels.com/photos/1417943/pexels-photo-1417943.jpeg"},
    {"id": 9, "name": "Samosa", "price": 40, "category": "food", "image_url": "https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg"},
    {"id": 10, "name": "Lemon Soda", "price": 35, "category": "drink", "image_url": "https://images.pexels.com/photos/338713/pexels-photo-338713.jpeg"},
]

@app.route('/api/health', methods=['GET'])
def health():
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        products_count = products_col.count_documents({})
        orders_count = orders_col.count_documents({})
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'products': products_count,
            'orders': orders_count,
            'message': 'MongoDB connected!'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': str(e)
        }), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    # Check if products exist, if not, seed them
    if products_col.count_documents({}) == 0:
        products_col.insert_many(SAMPLE_PRODUCTS)
    
    products = list(products_col.find({}, {'_id': 0}))  # Exclude MongoDB _id
    return jsonify(products)

@app.route('/api/order', methods=['POST'])
def create_order():
    try:
        data = request.json
        
        # Get product details
        product = next((p for p in SAMPLE_PRODUCTS if p['id'] == data['product_id']), None)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Create order
        order = {
            'product_id': data['product_id'],
            'product_name': product['name'],
            'product_price': product['price'],
            'customer_name': data['name'],
            'customer_phone': data['phone'],
            'customer_email': data.get('email', ''),
            'quantity': data.get('quantity', 1),
            'total_price': data.get('quantity', 1) * product['price'],
            'order_date': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        # Insert into MongoDB
        result = orders_col.insert_one(order)
        
        return jsonify({
            'message': 'Order placed successfully!',
            'order_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = list(orders_col.find())
    # Convert ObjectId to string for JSON
    for order in orders:
        order['_id'] = str(order['_id'])
    return jsonify(orders)

@app.route('/api/seed', methods=['POST'])
def seed_database():
    # Clear existing products
    products_col.delete_many({})
    # Insert sample products
    products_col.insert_many(SAMPLE_PRODUCTS)
    return jsonify({'message': f'Seeded {len(SAMPLE_PRODUCTS)} products'})

if __name__ == '__main__':
    print("🚀 Starting Mayabazar Backend with MongoDB...")
    print(f"📁 MongoDB URI: {mongo_uri}")
    app.run(host='0.0.0.0', port=5000, debug=True)
