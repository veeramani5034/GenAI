"""
Restaurant database utilities
"""

import json
import os

class RestaurantDB:
    def __init__(self, restaurants_file='data/restaurants.json'):
        self.restaurants_file = restaurants_file
        self.restaurants = self.load_restaurants()
    
    def load_restaurants(self):
        """Load restaurants from JSON file"""
        if os.path.exists(self.restaurants_file):
            with open(self.restaurants_file, 'r') as f:
                return json.load(f)
        return []
    
    def search_by_cuisine(self, cuisine):
        """Search restaurants by cuisine"""
        cuisine_lower = cuisine.lower()
        results = []
        for restaurant in self.restaurants:
            if any(cuisine_lower in c.lower() for c in restaurant['cuisine']):
                results.append(restaurant)
        return results
    
    def search_by_name(self, name):
        """Search restaurants by name"""
        name_lower = name.lower()
        results = []
        for restaurant in self.restaurants:
            if name_lower in restaurant['name'].lower():
                results.append(restaurant)
        return results
    
    def get_top_rated(self, limit=5):
        """Get top rated restaurants"""
        sorted_restaurants = sorted(
            self.restaurants, 
            key=lambda x: x['rating'], 
            reverse=True
        )
        return sorted_restaurants[:limit]
    
    def get_fastest_delivery(self, limit=5):
        """Get restaurants with fastest delivery"""
        sorted_restaurants = sorted(
            self.restaurants,
            key=lambda x: int(x['delivery_time'].split()[0])
        )
        return sorted_restaurants[:limit]
    
    def get_by_price_range(self, price_range):
        """Get restaurants by price range (₹, ₹₹, ₹₹₹)"""
        return [r for r in self.restaurants if r['price_range'] == price_range]
    
    def recommend_restaurants(self, preferences=None):
        """Recommend restaurants based on preferences"""
        if not preferences:
            return self.get_top_rated(3)
        
        # Simple recommendation logic
        results = []
        
        # Filter by cuisine if specified
        if 'cuisine' in preferences:
            results = self.search_by_cuisine(preferences['cuisine'])
        
        # Filter by price range if specified
        if 'price_range' in preferences and results:
            results = [r for r in results if r['price_range'] == preferences['price_range']]
        
        # Sort by rating
        results = sorted(results, key=lambda x: x['rating'], reverse=True)
        
        return results[:3] if results else self.get_top_rated(3)
    
    def format_restaurant_info(self, restaurant):
        """Format restaurant information for display"""
        return f"""
**{restaurant['name']}** ⭐ {restaurant['rating']}
Cuisine: {', '.join(restaurant['cuisine'])}
Delivery: {restaurant['delivery_time']} | Min Order: ₹{restaurant['min_order']}
Popular: {', '.join(restaurant['popular_dishes'][:3])}
Price: {restaurant['price_range']}
"""
