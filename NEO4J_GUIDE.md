# Neo4j & Graph Database Guide for Supply Chain Tracker

## 📚 Table of Contents
1. [What is Neo4j?](#what-is-neo4j)
2. [Graph Database Concepts](#graph-database-concepts)
3. [How Data Gets to Neo4j](#how-data-gets-to-neo4j)
4. [Cypher Query Language Basics](#cypher-query-language-basics)
5. [Queries for Your Project](#queries-for-your-project)
6. [Practical Examples](#practical-examples)
7. [Visualizing Your Data](#visualizing-your-data)

---

## What is Neo4j?

**Neo4j** is a **graph database** - a type of NoSQL database that stores data as:
- **Nodes** (like Supplier, Product) - think of them as entities/objects
- **Relationships** (like SUPPLIES) - connections between nodes
- **Properties** (like name, price) - attributes on nodes and relationships

### Why Use Neo4j for Supply Chain?

Traditional SQL databases use tables and rows. Neo4j uses **graphs** which are perfect for:
- ✅ Tracking relationships (Supplier → Product → Store)
- ✅ Finding connections (which suppliers affect which stores?)
- ✅ Complex queries (impact analysis, shortest paths)
- ✅ Visual representation of the supply chain

---

## Graph Database Concepts

### 1. Nodes (Vertices)
Think of nodes as **entities** in your system.

**In Our Project:**
```
(:Supplier)  - A supplier company
(:Product)   - A product item
(:Store)     - A retail store (your partner's work)
```

**Visual Representation:**
```
┌─────────────┐
│  Supplier   │  ← This is a NODE
│ name: "ABC" │  ← These are PROPERTIES
└─────────────┘
```

### 2. Relationships (Edges)
Connections between nodes with direction.

**In Our Project:**
```
(:Supplier)-[:SUPPLIES]->(:Product)
(:Product)-[:STOCKED_AT]->(:Store)
```

**Visual Representation:**
```
┌──────────┐           ┌──────────┐
│ Supplier │─SUPPLIES─>│ Product  │
└──────────┘           └──────────┘
```

### 3. Properties
Key-value pairs attached to nodes or relationships.

**Node Properties:**
```javascript
(:Supplier {
  uid: "abc123",
  name: "Tech Suppliers Inc",
  country: "USA",
  email: "contact@tech.com"
})
```

**Relationship Properties:**
```javascript
-[:SUPPLIES {
  unit_price: 25.50,
  lead_time_days: 7,
  since: "2025-01-15"
}]->
```

---

## How Data Gets to Neo4j

### The Flow: Browser → Django → Neo4j

```
┌─────────┐      ┌─────────┐      ┌──────────┐      ┌────────┐
│ Browser │─────>│  Views  │─────>│ neomodel │─────>│ Neo4j  │
│  (Form) │      │(Python) │      │  (ORM)   │      │   DB   │
└─────────┘      └─────────┘      └──────────┘      └────────┘
```

### Step-by-Step Example: Creating a Supplier

#### 1. User Fills Form
```html
<!-- In browser: supplier_form.html -->
<form method="post">
  <input name="name" value="ABC Corp">
  <input name="email" value="abc@corp.com">
  <button>Save</button>
</form>
```

#### 2. Django View Processes
```python
# In views.py
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            # Create supplier node
            supplier = Supplier(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email']
            ).save()  # ← This saves to Neo4j!
```

#### 3. neomodel Translates to Cypher
```cypher
CREATE (s:Supplier {
  uid: "generated-unique-id",
  name: "ABC Corp",
  email: "abc@corp.com",
  created_at: datetime()
})
RETURN s
```

#### 4. Neo4j Stores Data
The node is now in the graph database and can be queried!

---

## Cypher Query Language Basics

**Cypher** is Neo4j's query language (like SQL for relational databases).

### Basic Syntax

#### Pattern Matching
```cypher
(variable:Label {property: value})
```

**Examples:**
```cypher
(s:Supplier)              -- Any supplier node
(p:Product {sku: "P001"}) -- Product with specific SKU
(s:Supplier)-[:SUPPLIES]->(p:Product)  -- Supplier supplies product
```

### Core Commands

#### 1. CREATE - Add New Data
```cypher
-- Create a supplier
CREATE (s:Supplier {
  uid: "123",
  name: "Tech Corp",
  country: "France"
})
RETURN s
```

```cypher
-- Create a product
CREATE (p:Product {
  uid: "456",
  name: "Laptop",
  sku: "LAP-001",
  category: "Electronics"
})
RETURN p
```

```cypher
-- Create a relationship
MATCH (s:Supplier {name: "Tech Corp"})
MATCH (p:Product {sku: "LAP-001"})
CREATE (s)-[:SUPPLIES {
  unit_price: 500,
  lead_time_days: 10
}]->(p)
```

#### 2. MATCH - Find Existing Data
```cypher
-- Find all suppliers
MATCH (s:Supplier)
RETURN s

-- Find supplier by name
MATCH (s:Supplier {name: "Tech Corp"})
RETURN s

-- Find products in Electronics category
MATCH (p:Product {category: "Electronics"})
RETURN p.name, p.sku
```

#### 3. RETURN - What to Display
```cypher
-- Return full nodes
MATCH (s:Supplier)
RETURN s

-- Return specific properties
MATCH (s:Supplier)
RETURN s.name, s.country

-- Return count
MATCH (s:Supplier)
RETURN count(s) as total_suppliers
```

#### 4. WHERE - Filter Results
```cypher
-- Suppliers from specific country
MATCH (s:Supplier)
WHERE s.country = "USA"
RETURN s

-- Products with price > 100
MATCH (s)-[r:SUPPLIES]->(p:Product)
WHERE r.unit_price > 100
RETURN p.name, r.unit_price
```

#### 5. SET - Update Data
```cypher
-- Update supplier email
MATCH (s:Supplier {name: "Tech Corp"})
SET s.email = "new@techcorp.com"
RETURN s
```

#### 6. DELETE - Remove Data
```cypher
-- Delete all data (CAREFUL!)
MATCH (n)
DETACH DELETE n

-- Delete specific supplier
MATCH (s:Supplier {name: "Old Corp"})
DETACH DELETE s
```

---

## Queries for Your Project

### Viewing Data

#### 1. See All Suppliers
```cypher
MATCH (s:Supplier)
RETURN s.name, s.country, s.email
ORDER BY s.name
```

**What Django does:**
```python
suppliers = Supplier.nodes.all()
```

#### 2. See All Products
```cypher
MATCH (p:Product)
RETURN p.name, p.sku, p.category
ORDER BY p.name
```

**What Django does:**
```python
products = Product.nodes.all()
```

#### 3. View Supply Chain Relationships
```cypher
MATCH (s:Supplier)-[r:SUPPLIES]->(p:Product)
RETURN s.name as Supplier, 
       p.name as Product, 
       r.unit_price as Price,
       r.lead_time_days as LeadTime
```

**What Django does:**
```python
supplier = Supplier.nodes.get(uid="some-id")
products = supplier.supplies.all()  # Get all products this supplier supplies
```

### Counting & Statistics

#### 4. Count Suppliers
```cypher
MATCH (s:Supplier)
RETURN count(s) as TotalSuppliers
```

#### 5. Count Products per Supplier
```cypher
MATCH (s:Supplier)-[:SUPPLIES]->(p:Product)
RETURN s.name, count(p) as ProductCount
ORDER BY ProductCount DESC
```

#### 6. Find Suppliers Without Products
```cypher
MATCH (s:Supplier)
WHERE NOT (s)-[:SUPPLIES]->()
RETURN s.name
```

### Complex Queries

#### 7. Find All Paths from Supplier to Product
```cypher
MATCH path = (s:Supplier)-[:SUPPLIES]->(p:Product)
RETURN path
```

#### 8. Average Price per Supplier
```cypher
MATCH (s:Supplier)-[r:SUPPLIES]->(p:Product)
RETURN s.name, avg(r.unit_price) as AvgPrice
ORDER BY AvgPrice DESC
```

#### 9. Products from Multiple Suppliers
```cypher
MATCH (p:Product)<-[:SUPPLIES]-(s:Supplier)
WITH p, count(s) as supplierCount
WHERE supplierCount > 1
RETURN p.name, supplierCount
ORDER BY supplierCount DESC
```

---

## Practical Examples

### Example 1: Create Complete Supply Chain

```cypher
-- Step 1: Create Suppliers
CREATE (s1:Supplier {
  uid: "s001",
  name: "Global Electronics",
  country: "China",
  email: "contact@global.com"
})

CREATE (s2:Supplier {
  uid: "s002",
  name: "Euro Parts",
  country: "Germany",
  email: "info@europarts.de"
})

-- Step 2: Create Products
CREATE (p1:Product {
  uid: "p001",
  name: "Laptop",
  sku: "LAP-2024-01",
  category: "Electronics"
})

CREATE (p2:Product {
  uid: "p002",
  name: "Mouse",
  sku: "MOU-2024-01",
  category: "Accessories"
})

-- Step 3: Create Relationships
MATCH (s:Supplier {uid: "s001"})
MATCH (p:Product {uid: "p001"})
CREATE (s)-[:SUPPLIES {
  unit_price: 500.00,
  lead_time_days: 14,
  since: datetime()
}]->(p)

MATCH (s:Supplier {uid: "s001"})
MATCH (p:Product {uid: "p002"})
CREATE (s)-[:SUPPLIES {
  unit_price: 15.00,
  lead_time_days: 7,
  since: datetime()
}]->(p)

MATCH (s:Supplier {uid: "s002"})
MATCH (p:Product {uid: "p002"})
CREATE (s)-[:SUPPLIES {
  unit_price: 12.00,
  lead_time_days: 10,
  since: datetime()
}]->(p)
```

**Visual Result:**
```
┌───────────────────┐                    ┌──────────┐
│ Global Electronics│─────SUPPLIES──────>│  Laptop  │
│    (China)        │                    │ $500, 14d│
└───────────────────┘                    └──────────┘
         │
         │
         │ SUPPLIES ($15, 7d)
         ├─────────────────────────────┐
         │                             ▼
         │                    ┌─────────────┐
         │                    │    Mouse    │
         │                    │             │
         │                    └─────────────┘
         │                             ▲
┌───────────────────┐                  │
│    Euro Parts     │──SUPPLIES────────┘
│    (Germany)      │    ($12, 10d)
└───────────────────┘
```

### Example 2: Query This Supply Chain

#### Find cheapest supplier for Mouse
```cypher
MATCH (s:Supplier)-[r:SUPPLIES]->(p:Product {name: "Mouse"})
RETURN s.name, r.unit_price
ORDER BY r.unit_price ASC
LIMIT 1
```

**Result:** Euro Parts - $12.00

#### Find all products from Global Electronics
```cypher
MATCH (s:Supplier {name: "Global Electronics"})-[:SUPPLIES]->(p:Product)
RETURN p.name, p.sku
```

**Result:**
- Laptop (LAP-2024-01)
- Mouse (MOU-2024-01)

---

## Visualizing Your Data

### In Neo4j Browser (http://localhost:7474)

#### 1. View Everything
```cypher
MATCH (n)
RETURN n
LIMIT 25
```

#### 2. View Supply Chain Graph
```cypher
MATCH (s:Supplier)-[r:SUPPLIES]->(p:Product)
RETURN s, r, p
```

**You'll see:**
- Blue circles = Supplier nodes
- Orange circles = Product nodes  
- Arrows = SUPPLIES relationships
- Click on any node/relationship to see properties

#### 3. Focus on One Supplier
```cypher
MATCH (s:Supplier {name: "Tech Corp"})
OPTIONAL MATCH (s)-[r:SUPPLIES]->(p:Product)
RETURN s, r, p
```

---

## Common Operations in Your Application

### When You Create a Supplier (Django)

**Your Code:**
```python
supplier = Supplier(
    name="New Corp",
    email="new@corp.com"
).save()
```

**Neo4j Executes:**
```cypher
CREATE (s:Supplier {
  uid: "auto-generated-uuid",
  name: "New Corp",
  email: "new@corp.com",
  created_at: datetime(),
  updated_at: datetime()
})
```

### When You Link Supplier to Product (Django)

**Your Code:**
```python
supplier = Supplier.nodes.get(uid="abc123")
product = Product.nodes.get(uid="xyz789")
supplier.supplies.connect(product, {
    'unit_price': 100.00,
    'lead_time_days': 7
})
```

**Neo4j Executes:**
```cypher
MATCH (s:Supplier {uid: "abc123"})
MATCH (p:Product {uid: "xyz789"})
CREATE (s)-[:SUPPLIES {
  unit_price: 100.00,
  lead_time_days: 7,
  since: datetime()
}]->(p)
```

### When You View Supplier Details (Django)

**Your Code:**
```python
supplier = Supplier.nodes.get(uid="abc123")
products = supplier.supplies.all()
```

**Neo4j Executes:**
```cypher
-- Get supplier
MATCH (s:Supplier {uid: "abc123"})
RETURN s

-- Get related products
MATCH (s:Supplier {uid: "abc123"})-[:SUPPLIES]->(p:Product)
RETURN p
```

---

## Useful Queries for Testing

### 1. Check What's in Your Database
```cypher
// Count everything
MATCH (n)
RETURN labels(n) as NodeType, count(n) as Count

// Result example:
// NodeType      | Count
// ["Supplier"]  | 5
// ["Product"]   | 12
```

### 2. Find Orphaned Nodes
```cypher
// Suppliers with no products
MATCH (s:Supplier)
WHERE NOT (s)-[:SUPPLIES]->()
RETURN s.name

// Products with no suppliers
MATCH (p:Product)
WHERE NOT ()-[:SUPPLIES]->(p)
RETURN p.name, p.sku
```

### 3. Clear All Test Data
```cypher
MATCH (n)
DETACH DELETE n
```

⚠️ **WARNING:** This deletes EVERYTHING! Use carefully!

---

## Key Differences: SQL vs Cypher

| SQL (Relational)              | Cypher (Graph)                    |
|-------------------------------|-----------------------------------|
| Tables with rows & columns    | Nodes with properties             |
| Foreign keys for relationships| Direct relationship edges         |
| JOIN operations               | Pattern matching                  |
| Fixed schema                  | Flexible schema                   |
| `SELECT * FROM suppliers`     | `MATCH (s:Supplier) RETURN s`     |
| `INSERT INTO suppliers...`    | `CREATE (s:Supplier {...})`       |

---

## Tips & Best Practices

### 1. Always Use Labels
```cypher
// Good
MATCH (s:Supplier) RETURN s

// Bad (searches all nodes)
MATCH (s) WHERE s.name = "ABC" RETURN s
```

### 2. Use Properties for Filtering
```cypher
// Good (uses index)
MATCH (s:Supplier {name: "ABC"}) RETURN s

// Also good
MATCH (s:Supplier)
WHERE s.country = "USA"
RETURN s
```

### 3. Limit Large Results
```cypher
MATCH (n)
RETURN n
LIMIT 100  // Always limit when testing!
```

### 4. Use EXPLAIN to Understand Queries
```cypher
EXPLAIN
MATCH (s:Supplier)-[:SUPPLIES]->(p:Product)
RETURN s, p
```

---

## Summary

### What You Need to Remember:

1. **Nodes** = Things (Supplier, Product)
2. **Relationships** = Connections (SUPPLIES)
3. **Properties** = Attributes (name, price)
4. **neomodel** = Python library that translates your code to Cypher
5. **Cypher** = Query language for Neo4j
6. **Django does the translation** = You write Python, it becomes Cypher

### The Flow:
```
Python Code → neomodel → Cypher Query → Neo4j Database
```

### To Explore More:
1. Open Neo4j Browser: http://localhost:7474
2. Try the queries in this guide
3. Click on nodes to see their properties
4. Watch the graph grow as you add data!

---

## Quick Reference Card

```cypher
// View all suppliers
MATCH (s:Supplier) RETURN s

// View all products  
MATCH (p:Product) RETURN p

// View supply chain
MATCH (s:Supplier)-[r:SUPPLIES]->(p:Product) RETURN s, r, p

// Count nodes
MATCH (s:Supplier) RETURN count(s)

// Find by property
MATCH (s:Supplier {name: "ABC"}) RETURN s

// Delete all (CAREFUL!)
MATCH (n) DETACH DELETE n
```

---

**Happy graphing! 🚀**

For more information:
- [Neo4j Official Docs](https://neo4j.com/docs/)
- [Cypher Refcard](https://neo4j.com/docs/cypher-refcard/current/)
- [neomodel Docs](https://neomodel.readthedocs.io/)
