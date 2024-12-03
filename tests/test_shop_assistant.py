"""Tests for the shop assistant implementation."""

from src.product_catalog import get_product_info, check_stock

def test_get_product_info():
    """Test product info retrieval."""
    product = get_product_info("EcoFriendly Water Bottle")
    assert product["id"] == "ECO001"
    assert product["price"] == 24.99
    assert product["stock"] == 150

def test_check_stock():
    """Test stock checking."""
    stock = check_stock("EcoFriendly Water Bottle")
    assert stock == 150

def test_product_not_found():
    """Test handling of non-existent products."""
    assert get_product_info("NonExistent Product") is None
    assert check_stock("NonExistent Product") is None