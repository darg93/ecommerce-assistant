"""Mock product catalog data and functions."""

from typing import Dict, Optional

# Mock product catalog
PRODUCTS = [
    {
        "id": "ECO001",
        "name": "EcoFriendly Water Bottle",
        "description": "Sustainable 750ml stainless steel water bottle",
        "price": 24.99,
        "stock": 150
    },
    {
        "id": "TECH001", 
        "name": "Wireless Earbuds",
        "description": "High-quality wireless earbuds with noise cancellation",
        "price": 89.99,
        "stock": 75
    },
    {
        "id": "HOME001",
        "name": "Smart LED Bulb", 
        "description": "WiFi-enabled color changing LED bulb",
        "price": 19.99,
        "stock": 200
    },
    {
        "id": "SPORT001",
        "name": "Yoga Mat",
        "description": "Non-slip exercise yoga mat with carrying strap",
        "price": 29.99,
        "stock": 100
    },
    {
        "id": "LIFE001",
        "name": "Bamboo Cutlery Set",
        "description": "Eco-friendly portable bamboo cutlery set",
        "price": 15.99,
        "stock": 250
    }
]

def get_product_info(product_name: str) -> Optional[Dict]:
    """Get product information by name."""
    product_name = product_name.lower()
    for product in PRODUCTS:
        if product["name"].lower() == product_name:
            return product
    return None

def check_stock(product_name: str) -> Optional[int]:
    """Check stock availability for a product."""
    product = get_product_info(product_name)
    return product["stock"] if product else None