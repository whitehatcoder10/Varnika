# Varnika - Handicraft Platform

A modern platform connecting artisans with customers worldwide, featuring AI-powered product enhancement and voice-to-text capabilities.

## 🚀 Features

### For Sellers
- **Product Management**: Add, edit, and manage your handicraft products
- **AI Image Enhancement**: Automatically enhance product photos with professional backgrounds
- **Voice-to-Text**: Describe your products using voice input
- **AI Content Generation**: Get AI-generated product descriptions and Instagram captions
- **Real-time Dashboard**: View your products and manage inventory

### For Buyers
- **Product Discovery**: Browse products by category
- **Enhanced Shopping**: View AI-enhanced product images
- **Shopping Cart**: Add products and manage your cart
- **Product Details**: View detailed product information with AI-generated descriptions

## 🛠️ Technology Stack

### Backend
- **Python Flask**: RESTful API server
- **MySQL**: Database for product and user data
- **Google Cloud AI**: Image enhancement and content generation
- **Google Cloud Storage**: Image storage and management

### Frontend
- **React + TypeScript**: Modern web application
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Radix UI**: Accessible component library

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Google Cloud Platform account (for AI features)

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=artisan_platform
GCLOUD_PROJECT_ID=your_project_id
REGION=us-central1
GCS_BUCKET_NAME=your_bucket_name
```

Set up the database:
```bash
# Import the database schema
mysql -u root -p < Artisans_platform.sql

# Run migration to add missing fields
python migrate_database.py

# Start the backend server
python app.py
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Test the Integration

```bash
# Run the API test script
python test_integration.py
```

## 🔧 API Endpoints

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Add new product
- `GET /api/products/{id}` - Get specific product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### AI Features
- `POST /api/generate_content` - Generate product descriptions
- `POST /api/enhance_image` - Enhance product images

## 🎯 Usage

### Adding a Product (Seller)

1. Login as a seller
2. Navigate to "Add Product"
3. Fill in product details (name, price, category)
4. Add a description (text or voice input)
5. Upload a product image
6. Optionally enhance the image with AI
7. Submit the product

### Browsing Products (Buyer)

1. Login as a buyer
2. Browse products by category
3. View product details
4. Add products to cart
5. Manage your shopping cart

## 🔍 Testing

The integration includes comprehensive testing:

1. **API Testing**: Use `test_integration.py` to verify backend functionality
2. **Frontend Testing**: Manual testing through the web interface
3. **End-to-End Testing**: Complete seller workflow from product creation to display

## 📁 Project Structure

```
Varnika/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── database.py           # Database connection
│   ├── migrate_database.py   # Database migration script
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── services/
│   │   │   └── api.ts       # API service layer
│   │   └── components/      # UI components
│   └── package.json         # Node.js dependencies
├── Artisans_platform.sql    # Database schema
├── test_integration.py      # API testing script
└── setup_instructions.md    # Detailed setup guide
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please refer to the setup instructions or create an issue in the repository.
