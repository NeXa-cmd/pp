"""
Neo4j Models for Suppliers and Products using neomodel.

Models:
    - Supplier: Represents a supplier in the supply chain
    - Product: Represents a product
    - SUPPLIES: Relationship between Supplier and Product
"""

from neomodel import (
    StructuredNode,
    StringProperty,
    EmailProperty,
    DateTimeProperty,
    RelationshipTo,
    RelationshipFrom,
    StructuredRel,
    FloatProperty,
    IntegerProperty,
    UniqueIdProperty
)
from datetime import datetime


class SuppliesRel(StructuredRel):
    """
    Relationship properties for SUPPLIES relationship.
    Represents the supply contract between a supplier and a product.
    """
    since = DateTimeProperty(default=datetime.now)
    unit_price = FloatProperty()
    lead_time_days = IntegerProperty()


class Supplier(StructuredNode):
    """
    Supplier node in Neo4j.
    
    Properties:
        uid: Unique identifier
        name: Company name of the supplier
        contact_person: Name of the contact person
        email: Email address
        phone: Phone number
        address: Physical address
        country: Country of operation
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    contact_person = StringProperty()
    email = EmailProperty()
    phone = StringProperty()
    address = StringProperty()
    country = StringProperty()
    created_at = DateTimeProperty(default=datetime.now)
    updated_at = DateTimeProperty(default=datetime.now)
    
    # Relationships
    supplies = RelationshipTo('Product', 'SUPPLIES', model=SuppliesRel)
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'suppliers'


class Product(StructuredNode):
    """
    Product node in Neo4j.
    
    Properties:
        uid: Unique identifier
        name: Product name
        sku: Stock Keeping Unit (unique identifier)
        description: Product description
        category: Product category
        unit_of_measure: Unit of measurement (kg, pieces, liters, etc.)
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    sku = StringProperty(unique_index=True, required=True)
    description = StringProperty()
    category = StringProperty()
    unit_of_measure = StringProperty(default='pieces')
    created_at = DateTimeProperty(default=datetime.now)
    updated_at = DateTimeProperty(default=datetime.now)
    
    # Relationships
    supplied_by = RelationshipFrom('Supplier', 'SUPPLIES', model=SuppliesRel)
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    class Meta:
        app_label = 'suppliers'
