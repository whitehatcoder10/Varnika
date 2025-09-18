#!/usr/bin/env python3
"""
Test script to verify the backend API integration
"""

import requests
import json

API_BASE_URL = "http://localhost:5000/api"

def test_api_endpoints():
    """Test all API endpoints"""
    print("Testing Varnika Backend API Integration...")
    print("=" * 50)
    
    # Test 1: Get all products
    print("\n1. Testing GET /api/products")
    try:
        response = requests.get(f"{API_BASE_URL}/products")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: Found {len(data.get('products', []))} products")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return
    
    # Test 2: Add a new product
    print("\n2. Testing POST /api/products")
    test_product = {
        "name": "Test Handcrafted Vase",
        "price": 45.99,
        "category": "Pottery",
        "description": "A beautiful handmade ceramic vase with traditional patterns",
        "image_url": "https://example.com/test-image.jpg",
        "artisan_id": 1
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/products",
            json=test_product,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            data = response.json()
            product_id = data.get('product_id')
            print(f"✅ Success: Product added with ID {product_id}")
            
            # Test 3: Get specific product
            print(f"\n3. Testing GET /api/products/{product_id}")
            response = requests.get(f"{API_BASE_URL}/products/{product_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success: Retrieved product '{data['product']['name']}'")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
            
            # Test 4: Update product
            print(f"\n4. Testing PUT /api/products/{product_id}")
            update_data = {
                "name": "Updated Test Vase",
                "price": 55.99,
                "category": "Pottery",
                "description": "Updated description",
                "image_url": "https://example.com/updated-image.jpg"
            }
            response = requests.put(
                f"{API_BASE_URL}/products/{product_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print("✅ Success: Product updated")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
            
            # Test 5: Delete product
            print(f"\n5. Testing DELETE /api/products/{product_id}")
            response = requests.delete(f"{API_BASE_URL}/products/{product_id}")
            if response.status_code == 200:
                print("✅ Success: Product deleted")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Test content generation
    print("\n6. Testing POST /api/generate_content")
    try:
        content_data = {
            "product_type": "handmade pottery",
            "keywords": "ceramic, traditional, handcrafted"
        }
        response = requests.post(
            f"{API_BASE_URL}/generate_content",
            json=content_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Success: Content generated")
            print(f"   Description: {data.get('description', '')[:100]}...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("API Integration Test Complete!")

if __name__ == "__main__":
    test_api_endpoints()
