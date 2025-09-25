# Savannah Informatics Backend Assessment

E-commerce backend API built with Django REST Framework featuring hierarchical product categories, customer management, order processing with automated notifications.

## Features

- **REST API** for products, categories, customers, and orders
- **Hierarchical product categories** (unlimited depth)
- **Customer authentication** with OpenID Connect
- **Order processing** with automatic SMS and email notifications
- **Average price calculation** by category
- **Docker containerization**
- **Comprehensive testing**

## Technology Stack

- Python 3.8+
- Django 4.2
- Django REST Framework
- PostgreSQL
- OAuth2/OpenID Connect
- Africa's Talking SMS API
- Docker & Docker Compose

## Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd savannah-backend-assessment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```
### 2. Environment Setup
Create .env file:
``` bash
    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_URL=postgresql://user:pass@localhost/ecommerce_db
    AFRICAS_TALKING_USERNAME=your-username
    AFRICAS_TALKING_API_KEY=your-api-key
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD=your-app-password
    ADMIN_EMAIL=admin@company.com
```
### 3: Database Setup
run the below commands:
``` bash
    python manage.py migrate
    python manage.py createsuperuser
```

### 4: Running the development server
``` bash
python manage.py runserver
```

## DOCKER DEPLOYMENT
local development:
``` bash
    docker-compose up --build
```
production build:
``` bash
    docker build -t ecommerce-api .
    docker run -p 8000:8000 ecommerce-api
```

## API ENDPOINTS
- Products
    - **GET /api/products/** - List all products
    - **POST /api/products/** - Create product
    - **GET /api/products/{id}/** - Get product details
    - **GET /api/products/average_price_by_category/?category_id=1** - Average price by category

- Categories
    - **GET /api/categories/** - List categories (hierarchical)
    - **POST /api/categories/** - Create category

- Orders
    - **GET /api/orders/** - List orders
    - **POST /api/orders/** - Create order (triggers SMS + email)

- Authentication
    - **POST /o/token/** - Get OAuth2 token
    - **POST /o/revoke_token/** - Revoke token

### Example of API usage
``` bash
    curl -X POST http://localhost:8000/api/orders/ \
    -H "Content-Type: application/json" \
    -d '{
        "customer": 1,
        "items": [{"product_id": 1, "quantity": 2}],
        "notes": "Test order"
    }'
```
### For Testing Run the below commands
``` bash
    # Run all tests
    python manage.py test

    # Run with coverage
    pytest --cov=. --cov-report=html
```
## PROJECT STRUCTURE
``` 
savannah-backend-assessment/
├── ecommerce_api/          # Django project settings
├── products/               # Product & category models/APIs
├── customers/              # Customer management
├── orders/                 # Order processing & notifications
├── utils/                  # Utilities (SMS, email)
├── tests/                  # Test suites
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Multi-container setup
└── requirements.txt       # Python dependencies
```

### Key Features Implemented
1. Hierarchical Categories
```
    Products are organized in unlimited-depth categories using django-mptt:
        All Products
        ├── Bakery
        │   ├── Bread
        │   └── Cookies
        └── Produce
            ├── Fruits
            └── Vegetables
```
2. Order Processing
    When orders are created:
        - SMS sent to customer via Africa's Talking
        - Email notification sent to administrator
        - Order status tracking

3. Authentication
    - OAuth2/OpenID Connect implementation for secure API access.

4. Development Notes 
    - a. SMS functionality uses Africa's Talking sandbox for testing
    - b. Email notifications configured for Gmail SMTP
    - c. All API endpoints support pagination
    - d. Comprehensive error handling and logging
    - e. Follow Django best practices (DRY, KISS principles)

5. Deployment Considerations
    - a. Environment variables for sensitive data
    - b. PostgreSQL for production database
    - c. Docker for consistent deployments
    - d. Kubernetes manifests included for orchestration
