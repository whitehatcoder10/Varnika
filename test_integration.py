#!/usr/bin/env python3
"""
Test complete Varnika platform integration
"""

import requests
import json
import time

def test_backend_api():
    """Test backend API endpoints"""
    print("🔍 Testing Backend API")
    print("=" * 50)
    
    base_url = "http://localhost:5001/api"
    
    try:
        # Test products endpoint
        print("📦 Testing products endpoint...")
        response = requests.get(f"{base_url}/products", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"✅ Products endpoint working - {len(products)} products found")
            
            if products:
                print("📋 Sample products:")
                for i, product in enumerate(products[:3], 1):
                    print(f"  {i}. {product.get('name', 'Unknown')} - ₹{product.get('price', '0')}")
            
            return True
        else:
            print(f"❌ Products endpoint failed - Status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running - Please start with: cd backend && python app.py")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_frontend():
    """Test frontend accessibility"""
    print("\n🎨 Testing Frontend")
    print("=" * 50)
    
    try:
        # Test frontend
        print("🌐 Testing frontend accessibility...")
        response = requests.get("http://localhost:5173", timeout=10)
        
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend not accessible - Status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Frontend not running - Please start with: cd frontend && npm run dev")
        return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def test_database_integration():
    """Test database integration"""
    print("\n🗄️  Testing Database Integration")
    print("=" * 50)
    
    try:
        # Test specific product endpoint
        print("🔍 Testing specific product endpoint...")
        response = requests.get("http://localhost:5001/api/products/1", timeout=10)
        
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product details endpoint working")
            print(f"  Product: {product.get('name', 'Unknown')}")
            print(f"  Artisan: {product.get('artisan_name', 'Unknown')}")
            print(f"  Category: {product.get('category_name', 'Unknown')}")
            return True
        else:
            print(f"❌ Product details endpoint failed - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Database integration test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Varnika Platform Integration Test")
    print("=" * 60)
    
    # Wait a moment for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(2)
    
    # Run tests
    backend_ok = test_backend_api()
    frontend_ok = test_frontend()
    database_ok = test_database_integration()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    print(f"Backend API: {'✅ Working' if backend_ok else '❌ Failed'}")
    print(f"Frontend: {'✅ Working' if frontend_ok else '❌ Failed'}")
    print(f"Database Integration: {'✅ Working' if database_ok else '❌ Failed'}")
    
    if backend_ok and frontend_ok and database_ok:
        print("\n🎉 All tests passed! Varnika platform is fully integrated!")
        print("\n🌐 Access your application:")
        print("  Frontend: http://localhost:5173")
        print("  Backend API: http://localhost:5001/api")
        print("\n✨ Features available:")
        print("  • View products from Cloud SQL")
        print("  • Add new products with AI descriptions")
        print("  • Image upload and enhancement")
        print("  • Voice-to-text input")
        print("  • Category filtering")
        print("  • Artisan management")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        
        if not backend_ok:
            print("\n🔧 To fix backend:")
            print("  cd backend && python app.py")
            
        if not frontend_ok:
            print("\n🔧 To fix frontend:")
            print("  cd frontend && npm run dev")

if __name__ == "__main__":
    main()