from datetime import datetime
from typing import Dict, List

class ShopDatabase:
    def __init__(self):
        # Mock products database
        self.products_db = {
            "iPhone 15": {
                "price": 5999,
                "stock": 500,
                "description": "Latest iPhone with A16 chip, superior performance",
                "category": "Mobile Phones",
                "rating": 4.8,
                "review_count": 2345,
                "specs": ["128GB", "256GB", "512GB"],
                "colors": ["Midnight", "Starlight", "Blue"],
                "brand": "Apple",
                "reviews": [
                    {"user": "USER001", "rating": 5, "content": "Great phone, excellent camera", "date": "2024-02-28"},
                    {"user": "USER002", "rating": 4, "content": "Good overall, battery life could be better", "date": "2024-02-29"}
                ]
            },
            "iPhone 15 Pro": {
                "price": 8999,
                "stock": 300,
                "description": "Pro camera system, Titanium design, A17 Pro chip",
                "category": "Mobile Phones",
                "rating": 4.9,
                "review_count": 1567,
                "specs": ["256GB", "512GB", "1TB"],
                "colors": ["Natural Titanium", "Blue Titanium", "Black Titanium"],
                "brand": "Apple",
                "reviews": [
                    {"user": "USER005", "rating": 5, "content": "Best iPhone ever, amazing camera system", "date": "2024-02-25"}
                ]
            },
            "Huawei Mate60": {
                "price": 6999,
                "stock": 200,
                "description": "Latest Huawei flagship with Kirin chip",
                "category": "Mobile Phones",
                "rating": 4.9,
                "review_count": 1890,
                "specs": ["256GB", "512GB"],
                "colors": ["Black", "Gray", "White"],
                "brand": "Huawei",
                "reviews": [
                    {"user": "USER003", "rating": 5, "content": "Excellent signal strength", "date": "2024-03-01"}
                ]
            },
            "Xiaomi 14 Pro": {
                "price": 4999,
                "stock": 800,
                "description": "Snapdragon 8 Gen 3, Leica optics",
                "category": "Mobile Phones",
                "rating": 4.7,
                "review_count": 3456,
                "specs": ["256GB", "512GB"],
                "colors": ["Black", "White", "Green"],
                "brand": "Xiaomi",
                "reviews": [
                    {"user": "USER006", "rating": 4, "content": "Great value flagship", "date": "2024-03-05"}
                ]
            },
            "Samsung S24 Ultra": {
                "price": 9999,
                "stock": 400,
                "description": "Ultimate Galaxy experience with S Pen",
                "category": "Mobile Phones",
                "rating": 4.8,
                "review_count": 890,
                "specs": ["256GB", "512GB", "1TB"],
                "colors": ["Titanium Black", "Titanium Gray", "Titanium Violet"],
                "brand": "Samsung",
                "reviews": [
                    {"user": "USER007", "rating": 5, "content": "Best Android phone", "date": "2024-03-10"}
                ]
            },
            "Xiaomi Band 8": {
                "price": 299,
                "stock": 1000,
                "description": "24/7 health monitoring with long battery life",
                "category": "Wearables",
                "rating": 4.7,
                "review_count": 5678,
                "specs": ["Standard", "NFC"],
                "colors": ["Black", "Blue"],
                "brand": "Xiaomi",
                "reviews": [
                    {"user": "USER004", "rating": 5, "content": "Great value for money", "date": "2024-03-02"}
                ]
            },
            "Apple Watch Series 9": {
                "price": 3299,
                "stock": 600,
                "description": "Advanced health features with S9 chip",
                "category": "Wearables",
                "rating": 4.8,
                "review_count": 2789,
                "specs": ["GPS", "GPS + Cellular"],
                "colors": ["Midnight", "Starlight", "Silver", "Pink"],
                "brand": "Apple",
                "reviews": [
                    {"user": "USER008", "rating": 5, "content": "Perfect companion for iPhone", "date": "2024-03-08"}
                ]
            },
            "AirPods Pro 2": {
                "price": 1899,
                "stock": 750,
                "description": "Active Noise Cancellation, Adaptive Audio",
                "category": "Audio",
                "rating": 4.8,
                "review_count": 4567,
                "specs": ["USB-C"],
                "colors": ["White"],
                "brand": "Apple",
                "reviews": [
                    {"user": "USER009", "rating": 5, "content": "Best wireless earbuds", "date": "2024-03-07"}
                ]
            },
            "MacBook Pro 14": {
                "price": 14999,
                "stock": 200,
                "description": "M3 Pro chip, 14-inch Liquid Retina XDR display",
                "category": "Laptops",
                "rating": 4.9,
                "review_count": 1234,
                "specs": ["512GB", "1TB", "2TB"],
                "colors": ["Space Black", "Silver"],
                "brand": "Apple",
                "reviews": [
                    {"user": "USER010", "rating": 5, "content": "Perfect for developers", "date": "2024-03-09"}
                ]
            }
        }
        
        # Mock orders database
        self.orders_db = {
            "ORDER2024030001": {
                "user_id": "USER001",
                "product": "iPhone 15",
                "quantity": 1,
                "total_price": 5999,
                "status": "Shipped",
                "tracking_number": "SF1234567890",
                "order_time": "2024-03-01 10:30:00",
                "payment_status": "Paid",
                "shipping_address": "XX Street, Chaoyang District, Beijing",
                "contact_phone": "13800138000"
            },
            "ORDER2024030002": {
                "user_id": "USER002",
                "product": "Huawei Mate60",
                "quantity": 1,
                "total_price": 6999,
                "status": "Pending Shipment",
                "tracking_number": "",
                "order_time": "2024-03-02 15:20:00",
                "payment_status": "Paid",
                "shipping_address": "XX Road, Pudong District, Shanghai",
                "contact_phone": "13900139000"
            },
            "ORDER2024030003": {
                "user_id": "USER003",
                "product": "MacBook Pro 14",
                "quantity": 1,
                "total_price": 14999,
                "status": "Delivered",
                "tracking_number": "SF1234567891",
                "order_time": "2024-03-03 09:15:00",
                "payment_status": "Paid",
                "shipping_address": "XX Avenue, Tianhe District, Guangzhou",
                "contact_phone": "13600136000"
            },
            "ORDER2024030004": {
                "user_id": "USER004",
                "product": "AirPods Pro 2",
                "quantity": 1,
                "total_price": 1899,
                "status": "Processing",
                "tracking_number": "",
                "order_time": "2024-03-04 14:20:00",
                "payment_status": "Pending",
                "shipping_address": "XX Road, Jingan District, Shanghai",
                "contact_phone": "13700137000"
            },
            "ORDER2024030005": {
                "user_id": "USER005",
                "product": "iPhone 15 Pro",
                "quantity": 1,
                "total_price": 8999,
                "status": "Cancelled",
                "tracking_number": "",
                "order_time": "2024-03-05 11:30:00",
                "payment_status": "Refunded",
                "shipping_address": "XX Street, Haidian District, Beijing",
                "contact_phone": "13500135000"
            }
        }
        
        # Mock logistics database
        self.logistics_db = {
            "SF1234567890": [
                {"time": "2024-03-01 12:00:00", "status": "Picked Up", "location": "Chaoyang District Transfer Center"},
                {"time": "2024-03-01 15:30:00", "status": "In Transit", "location": "Shunyi District Transfer Center"},
                {"time": "2024-03-02 09:00:00", "status": "Out for Delivery", "location": "Chaoyang District"}
            ],
            "SF1234567891": [
                {"time": "2024-03-03 10:00:00", "status": "Picked Up", "location": "Guangzhou Central Hub"},
                {"time": "2024-03-03 14:30:00", "status": "In Transit", "location": "Guangzhou Airport"},
                {"time": "2024-03-03 20:00:00", "status": "Arrived", "location": "Tianhe District Center"},
                {"time": "2024-03-04 09:00:00", "status": "Delivered", "location": "Recipient Address"}
            ]
        }
        
        # Mock shopping cart database
        self.cart_db = {
            "USER001": [
                {"product": "Xiaomi Band 8", "quantity": 1, "spec": "NFC", "color": "Black"},
                {"product": "AirPods Pro 2", "quantity": 1, "spec": "USB-C", "color": "White"}
            ],
            "USER002": [
                {"product": "iPhone 15", "quantity": 1, "spec": "256GB", "color": "Starlight"},
                {"product": "Xiaomi Band 8", "quantity": 2, "spec": "Standard", "color": "Blue"}
            ],
            "USER003": [
                {"product": "MacBook Pro 14", "quantity": 1, "spec": "1TB", "color": "Space Black"}
            ],
            "USER004": [
                {"product": "Samsung S24 Ultra", "quantity": 1, "spec": "512GB", "color": "Titanium Black"},
                {"product": "Apple Watch Series 9", "quantity": 1, "spec": "GPS", "color": "Midnight"}
            ]
        }
        
        # Mock coupon database
        self.coupon_db = {
            "USER001": [
                {"code": "DISC100", "type": "Amount Off", "amount": 100, "condition": "Min. spend 1000", "valid_until": "2024-12-31"},
                {"code": "DISC50", "type": "No Minimum", "amount": 50, "condition": "No minimum spend", "valid_until": "2024-06-30"}
            ],
            "USER002": [
                {"code": "NEWUSER200", "type": "Amount Off", "amount": 200, "condition": "Min. spend 2000", "valid_until": "2024-12-31"}
            ],
            "USER003": [
                {"code": "APPLE500", "type": "Amount Off", "amount": 500, "condition": "Min. spend 5000 on Apple products", "valid_until": "2024-06-30"},
                {"code": "BDAY100", "type": "No Minimum", "amount": 100, "condition": "Birthday special", "valid_until": "2024-03-15"}
            ],
            "USER004": [
                {"code": "VIP300", "type": "Amount Off", "amount": 300, "condition": "VIP exclusive", "valid_until": "2024-12-31"}
            ]
        }

    def get_product_info(self, product_name: str) -> Dict:
        """Query product information"""
        return self.products_db.get(product_name, {})
    
    def get_order_info(self, order_id: str) -> Dict:
        """Query order information"""
        return self.orders_db.get(order_id, {})
    
    def get_logistics_info(self, tracking_number: str) -> List:
        """Query logistics information"""
        return self.logistics_db.get(tracking_number, [])
    
    def search_products(self, category: str = None, price_range: tuple = None) -> List[Dict]:
        """Search products"""
        results = []
        for name, info in self.products_db.items():
            if category and info["category"] != category:
                continue
            if price_range:
                min_price, max_price = price_range
                if not (min_price <= info["price"] <= max_price):
                    continue
            results.append({"product_name": name, **info})
        return results
    
    def get_cart_items(self, user_id: str) -> List[Dict]:
        """Get user's shopping cart items"""
        return self.cart_db.get(user_id, [])
    
    def add_to_cart(self, user_id: str, product: str, quantity: int, spec: str, color: str) -> bool:
        """Add item to shopping cart"""
        if user_id not in self.cart_db:
            self.cart_db[user_id] = []
        
        self.cart_db[user_id].append({
            "product": product,
            "quantity": quantity,
            "spec": spec,
            "color": color
        })
        return True
    
    def get_user_coupons(self, user_id: str) -> List[Dict]:
        """Get user's coupons"""
        return self.coupon_db.get(user_id, [])
    
    def create_order(self, user_id: str, product: str, quantity: int, address: str, phone: str) -> str:
        """Create new order"""
        order_id = f"ORDER{datetime.now().strftime('%Y%m%d%H%M%S')}"
        product_info = self.get_product_info(product)
        
        if not product_info:
            return ""
            
        total_price = product_info["price"] * quantity
        
        self.orders_db[order_id] = {
            "user_id": user_id,
            "product": product,
            "quantity": quantity,
            "total_price": total_price,
            "status": "Pending Payment",
            "tracking_number": "",
            "order_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "payment_status": "Unpaid",
            "shipping_address": address,
            "contact_phone": phone
        }
        
        return order_id