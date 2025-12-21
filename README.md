# Supply Chain Tracker - Supplier & Product Management

> **Your Part**: Infrastructure, Authentication, Suppliers, and Products
> 
> **Not Included**: Stores, Stock Management, Dashboard, Impact Analysis (handled by your partner)

## 📋 Project Overview

A Supply Chain Tracker built with Django and Neo4j to track the flow from Suppliers → Products → Stores (store management by partner).

## 🛠️ Tech Stack

- **Python**: 3.10+
- **Django**: 4.2.8
- **Neo4j**: 5.15.0 (Graph Database)
- **neomodel**: 5.2.1 (Neo4j ORM)
- **Bootstrap**: 5.3.0
- **Docker**: For containerization

## 📁 Project Structure

```
pp/
├── docker-compose.yml          # Docker configuration for Django & Neo4j
├── Dockerfile                  # Django app container
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── manage.py                   # Django management script
│
├── supply_chain/               # Django project settings
│   ├── __init__.py
│   ├── settings.py            # Configured with Neo4j connection
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── suppliers/                  # Main app for Suppliers & Products
│   ├── models.py              # Neo4j models (Supplier, Product, SUPPLIES)
│   ├── views.py               # All CRUD views
│   ├── forms.py               # Django forms
│   ├── urls.py                # App URL routing
│   ├── apps.py
│   ├── admin.py
│   ├── tests.py
│   └── templates/
│       └── suppliers/
│           ├── supplier_list.html
│           ├── supplier_form.html
│           ├── supplier_detail.html
│           ├── product_list.html
│           ├── product_form.html
│           ├── product_detail.html
│           └── link_supplier_product.html
│
└── templates/
    └── base.html              # Master template with Bootstrap navbar
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.10+ (for local development)

### 1. Start with Docker (Recommended)

```powershell
# Navigate to project directory
cd C:\Users\V22\Desktop\pp

# Build and start containers
docker-compose up --build

# Wait for Neo4j to fully start (about 30 seconds)
# Access the application at: http://localhost:8000
# Access Neo4j Browser at: http://localhost:7474
```

**Neo4j Credentials:**
- Username: `neo4j`
- Password: `password123`

### 2. Local Development Setup (Without Docker)

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Make sure Neo4j is running locally or update .env file
# Start Django development server
python manage.py runserver
```

## 📊 Neo4j Graph Schema

### Nodes

**Supplier**
```cypher
(:Supplier {
    uid: String (unique),
    name: String (required, unique),
    contact_person: String,
    email: String,
    phone: String,
    address: String,
    country: String,
    created_at: DateTime,
    updated_at: DateTime
})
```

**Product**
```cypher
(:Product {
    uid: String (unique),
    name: String (required),
    sku: String (required, unique),
    description: String,
    category: String,
    unit_of_measure: String,
    created_at: DateTime,
    updated_at: DateTime
})
```

### Relationship

```cypher
(:Supplier)-[:SUPPLIES {
    since: DateTime,
    unit_price: Float,
    lead_time_days: Integer
}]->(:Product)
```

## 🎯 Features Implemented

### ✅ Infrastructure
- [x] Docker Compose setup with Django and Neo4j 5.x
- [x] Django project configuration
- [x] Neo4j connection via neomodel
- [x] Bootstrap 5 master template with navbar

### ✅ Supplier Management
- [x] List all suppliers
- [x] Create new supplier
- [x] View supplier details
- [x] Edit supplier information
- [x] Delete supplier
- [x] View products supplied by each supplier

### ✅ Product Management
- [x] List all products
- [x] Create new product
- [x] View product details
- [x] Edit product information
- [x] Delete product
- [x] View suppliers for each product

### ✅ Relationship Management
- [x] Link Supplier to Product (SUPPLIES relationship)
- [x] Store relationship properties (unit price, lead time)
- [x] View supplier-product connections

### 🚫 Not Implemented (Partner's Responsibility)
- Stores management
- Stock management
- Dashboard
- Impact analysis

## 🌐 Available URLs

### Suppliers
- `/suppliers/` - List all suppliers
- `/suppliers/create/` - Create new supplier
- `/suppliers/<uid>/` - View supplier details
- `/suppliers/<uid>/edit/` - Edit supplier
- `/suppliers/<uid>/delete/` - Delete supplier

### Products
- `/suppliers/products/` - List all products
- `/suppliers/products/create/` - Create new product
- `/suppliers/products/<uid>/` - View product details
- `/suppliers/products/<uid>/edit/` - Edit product
- `/suppliers/products/<uid>/delete/` - Delete product

### Relationships
- `/suppliers/link/supplier-product/` - Link supplier to product

## 🎨 UI Features

- **Responsive Design**: Bootstrap 5 responsive grid
- **Icons**: Bootstrap Icons throughout
- **Navigation**: Clean navbar with placeholder links for partner's sections
- **Messages**: Django messages framework for user feedback
- **Cards & Tables**: Modern UI components
- **Forms**: Styled with Bootstrap form controls

## 🔧 Configuration

### Environment Variables (.env)

```env
NEO4J_BOLT_URL=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password123
SECRET_KEY=your-secret-key
DEBUG=True
```

### Neo4j Connection

The connection is configured in `supply_chain/settings.py`:

```python
neomodel_config.DATABASE_URL = f'bolt://{NEO4J_USERNAME}:{NEO4J_PASSWORD}@{NEO4J_BOLT_URL.split("//")[1]}'
```

## 📝 Usage Examples

### Create a Supplier
1. Navigate to `/suppliers/`
2. Click "Add New Supplier"
3. Fill in the form (only name is required)
4. Click "Save Supplier"

### Create a Product
1. Navigate to `/suppliers/products/`
2. Click "Add New Product"
3. Enter name and unique SKU (both required)
4. Optionally add description, category, and unit of measure
5. Click "Save Product"

### Link Supplier to Product
1. Make sure you have at least one supplier and one product
2. Navigate to `/suppliers/link/supplier-product/`
3. Select a supplier and a product from dropdowns
4. Optionally add unit price and lead time
5. Click "Create Link"

## 🧪 Testing with Neo4j Browser

Access Neo4j Browser at `http://localhost:7474` and run queries:

```cypher
// View all suppliers
MATCH (s:Supplier) RETURN s

// View all products
MATCH (p:Product) RETURN p

// View supply chain relationships
MATCH (s:Supplier)-[r:SUPPLIES]->(p:Product)
RETURN s, r, p

// Find products supplied by a specific supplier
MATCH (s:Supplier {name: "Your Supplier"})-[:SUPPLIES]->(p:Product)
RETURN p.name, p.sku
```

## 🤝 Integration Points for Partner

Your partner will need to:

1. **Create a new Django app** for stores (e.g., `stores/`)
2. **Define Store model** in neomodel with relationship to Product
3. **Add their URLs** to `supply_chain/urls.py`
4. **Update navbar links** in `templates/base.html` to point to their views
5. **Create Dashboard views** and update the Dashboard link

The base template already has placeholder links ready for:
- Stores (currently `#`)
- Dashboard (currently `#`)

## 📦 Dependencies

See `requirements.txt` for full list:
- Django 4.2.8
- neomodel 5.2.1
- django-neomodel 0.1.1
- neo4j 5.15.0
- python-dotenv 1.0.0

## 🐛 Troubleshooting

### Neo4j Connection Issues
- Ensure Neo4j container is fully started (wait ~30 seconds after `docker-compose up`)
- Check credentials in `.env` match those in `docker-compose.yml`
- Verify Neo4j is accessible at `bolt://localhost:7687`

### Django Issues
- Run `docker-compose logs web` to see Django logs
- Ensure all environment variables are properly set
- Check that `suppliers` app is in `INSTALLED_APPS`

### Port Conflicts
- Neo4j HTTP: 7474
- Neo4j Bolt: 7687
- Django: 8000

Make sure these ports are available on your system.

## 📄 License

This is a university project. All rights reserved.

## 👥 Team

- **Marouane (You)**: Infrastructure, Suppliers, Products
- **Partner**: Stores, Stock Management, Dashboard, Impact Analysis

---

**Status**: ✅ Your part is complete and ready for integration with your partner's code!
