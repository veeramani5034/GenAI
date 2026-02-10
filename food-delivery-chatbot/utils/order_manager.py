"""
Order management utilities
"""

import json
import os
from datetime import datetime, timedelta

class OrderManager:
    def __init__(self, orders_file='data/orders.json'):
        self.orders_file = orders_file
        self.orders = self.load_orders()
    
    def load_orders(self):
        """Load orders from JSON file"""
        if os.path.exists(self.orders_file):
            with open(self.orders_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_orders(self):
        """Save orders to JSON file"""
        with open(self.orders_file, 'w') as f:
            json.dump(self.orders, f, indent=2)
    
    def get_order(self, order_id):
        """Get order by ID"""
        for order in self.orders:
            if order['order_id'] == str(order_id):
                return order
        return None
    
    def get_order_status(self, order_id):
        """Get formatted order status"""
        order = self.get_order(order_id)
        if not order:
            return None
        
        status_messages = {
            'confirmed': 'Your order has been confirmed and sent to the restaurant.',
            'preparing': 'Your order is being prepared at the restaurant.',
            'out_for_delivery': 'Your order is on the way! Our delivery partner is heading to you.',
            'delivered': 'Your order has been delivered. Enjoy your meal!',
            'cancelled': 'This order has been cancelled.'
        }
        
        status_msg = status_messages.get(order['status'], 'Status unknown')
        
        return {
            'order_id': order['order_id'],
            'restaurant': order['restaurant'],
            'items': order['items'],
            'total': order['total'],
            'status': order['status'],
            'status_message': status_msg,
            'estimated_delivery': order['estimated_delivery'],
            'delivery_address': order['delivery_address']
        }
    
    def initiate_refund(self, order_id, reason=''):
        """Initiate refund for an order"""
        order = self.get_order(order_id)
        if not order:
            return None
        
        # In real system, this would integrate with payment gateway
        refund_info = {
            'order_id': order_id,
            'amount': order['total'],
            'status': 'initiated',
            'reason': reason,
            'initiated_at': datetime.now().isoformat(),
            'expected_completion': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        }
        
        # Update order status
        order['status'] = 'refund_initiated'
        self.save_orders()
        
        return refund_info
    
    def cancel_order(self, order_id):
        """Cancel an order"""
        order = self.get_order(order_id)
        if not order:
            return False
        
        # Can only cancel if not delivered
        if order['status'] in ['delivered', 'cancelled']:
            return False
        
        order['status'] = 'cancelled'
        self.save_orders()
        return True
    
    def update_delivery_address(self, order_id, new_address):
        """Update delivery address"""
        order = self.get_order(order_id)
        if not order:
            return False
        
        # Can only update if not out for delivery or delivered
        if order['status'] in ['out_for_delivery', 'delivered']:
            return False
        
        order['delivery_address'] = new_address
        self.save_orders()
        return True
    
    def get_recent_orders(self, customer_name=None, limit=5):
        """Get recent orders"""
        if customer_name:
            filtered = [o for o in self.orders if o['customer_name'] == customer_name]
            return filtered[:limit]
        return self.orders[:limit]
