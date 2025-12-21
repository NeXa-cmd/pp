# Supply Chain Tracker - Management Commands
# Run these in PowerShell from the project root

# ========================================
# DOCKER COMMANDS
# ========================================

# Start all services (first time or after changes)
docker-compose up --build

# Start services (subsequent times)
docker-compose up

# Start in detached mode (background)
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# View logs
docker-compose logs -f web      # Django logs
docker-compose logs -f neo4j    # Neo4j logs

# ========================================
# LOCAL DEVELOPMENT COMMANDS
# ========================================

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python manage.py runserver

# ========================================
# DJANGO MANAGEMENT COMMANDS
# ========================================

# Run Django shell (with neomodel access)
python manage.py shell

# Example shell commands:
# >>> from suppliers.models import Supplier, Product
# >>> suppliers = Supplier.nodes.all()
# >>> for s in suppliers:
# ...     print(s.name)

# ========================================
# NEO4J USEFUL QUERIES
# ========================================

# Run these in Neo4j Browser (http://localhost:7474)

# View all nodes and relationships
MATCH (n) RETURN n LIMIT 25

# View supply chain
MATCH (s:Supplier)-[r:SUPPLIES]->(p:Product)
RETURN s.name, p.name, r.unit_price, r.lead_time_days

# Count suppliers
MATCH (s:Supplier) RETURN count(s)

# Count products
MATCH (p:Product) RETURN count(p)

# Find suppliers without products
MATCH (s:Supplier)
WHERE NOT (s)-[:SUPPLIES]->()
RETURN s.name

# Find products without suppliers
MATCH (p:Product)
WHERE NOT ()-[:SUPPLIES]->(p)
RETURN p.name, p.sku

# Delete all data (CAREFUL!)
MATCH (n) DETACH DELETE n

# ========================================
# TESTING WORKFLOW
# ========================================

# 1. Start services
docker-compose up --build

# 2. Access application
# http://localhost:8000

# 3. Create test data
# - Navigate to http://localhost:8000/suppliers/create/
# - Create a supplier
# - Navigate to http://localhost:8000/suppliers/products/create/
# - Create a product
# - Navigate to http://localhost:8000/suppliers/link/supplier-product/
# - Link them together

# 4. Verify in Neo4j Browser
# http://localhost:7474
# Run: MATCH (s)-[r]->(p) RETURN s, r, p

# ========================================
# TROUBLESHOOTING
# ========================================

# Check if ports are in use
netstat -ano | findstr :8000
netstat -ano | findstr :7474
netstat -ano | findstr :7687

# Kill process by PID
taskkill /PID <PID> /F

# Rebuild containers from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up

# Check Docker container status
docker ps

# Access Django container shell
docker exec -it supply_chain_web bash

# Access Neo4j container shell
docker exec -it supply_chain_neo4j bash

# ========================================
# INTEGRATION WITH PARTNER'S CODE
# ========================================

# Your partner should:
# 1. Create new app: python manage.py startapp stores
# 2. Add 'stores' to INSTALLED_APPS in settings.py
# 3. Create Store model in stores/models.py using neomodel
# 4. Add stores URLs to supply_chain/urls.py
# 5. Update navbar links in templates/base.html
# 6. Create their views and templates

# ========================================
# PRODUCTION CHECKLIST (Later)
# ========================================

# Before deploying to production:
# [ ] Change SECRET_KEY in .env
# [ ] Set DEBUG=False in .env
# [ ] Change Neo4j password
# [ ] Add ALLOWED_HOSTS in settings.py
# [ ] Use environment-specific docker-compose files
# [ ] Set up proper logging
# [ ] Configure static files serving
# [ ] Set up SSL/TLS
# [ ] Regular backups of Neo4j data
