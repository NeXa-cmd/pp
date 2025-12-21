# Quick Setup Guide

## Windows PowerShell Commands

### Option 1: Docker Setup (Recommended)

```powershell
# Navigate to project directory
cd C:\Users\V22\Desktop\pp

# Build and start all services
docker-compose up --build

# In a new terminal, wait 30 seconds, then access:
# - Application: http://localhost:8000
# - Neo4j Browser: http://localhost:7474 (user: neo4j, password: password123)
```

### Option 2: Local Development

```powershell
# Navigate to project directory
cd C:\Users\V22\Desktop\pp

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Make sure Neo4j is running (Docker or local installation)
# Then start Django
python manage.py runserver

# Access at: http://localhost:8000
```

## First Time Setup Steps

1. **Start the services**
   ```powershell
   docker-compose up --build
   ```

2. **Wait for Neo4j to initialize** (about 30 seconds)

3. **Access the application**
   - Open browser: http://localhost:8000
   - You'll be redirected to the Suppliers page

4. **Create your first supplier**
   - Click "Add New Supplier"
   - Fill in at least the name field
   - Click "Save Supplier"

5. **Create your first product**
   - Click "Products" in navbar
   - Click "Add New Product"
   - Fill in name and SKU
   - Click "Save Product"

6. **Link supplier to product**
   - Click "Link Supplier to Product" button
   - Select a supplier and product
   - Optionally add price and lead time
   - Click "Create Link"

## Verify Neo4j Data

1. Open Neo4j Browser: http://localhost:7474
2. Login with:
   - Username: `neo4j`
   - Password: `password123`
3. Run query:
   ```cypher
   MATCH (s:Supplier)-[r:SUPPLIES]->(p:Product)
   RETURN s, r, p
   ```

## Stop Services

```powershell
# Press Ctrl+C in the terminal where docker-compose is running
# Or run:
docker-compose down
```

## Troubleshooting

### If port 8000 is already in use:
```powershell
# Find and kill the process
netstat -ano | findstr :8000
# Note the PID and kill it
taskkill /PID <PID> /F
```

### If Neo4j won't start:
```powershell
# Remove old volumes and restart
docker-compose down -v
docker-compose up --build
```

### If you see "No module named 'neomodel'":
```powershell
# Make sure you're in the virtual environment
.\venv\Scripts\Activate
pip install -r requirements.txt
```

## Next Steps for Your Partner

Your partner should:
1. Create a new Django app called `stores`
2. Define Store model and relationships to Product
3. Add their URLs to the project
4. Update the navbar links in base.html
5. Create dashboard views

The foundation is ready for integration!
