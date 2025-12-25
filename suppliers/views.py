"""
Views for Supplier and Product management.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from neomodel import db
from datetime import datetime

from .models import Supplier, Product, Store
from .forms import SupplierForm, ProductForm, LinkSupplierProductForm, StoreForm, StockAssignmentForm


# ==================== SUPPLIER VIEWS ====================

def supplier_list(request):
    """Display list of all suppliers."""
    suppliers = Supplier.nodes.all()
    return render(request, 'suppliers/supplier_list.html', {
        'suppliers': suppliers
    })


def supplier_create(request):
    """Create a new supplier."""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            try:
                # Create supplier node
                supplier = Supplier(
                    name=form.cleaned_data['name'],
                    contact_person=form.cleaned_data['contact_person'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    country=form.cleaned_data['country']
                ).save()
                
                messages.success(request, f'Supplier "{supplier.name}" created successfully!')
                return redirect('supplier_list')
            except Exception as e:
                messages.error(request, f'Error creating supplier: {str(e)}')
    else:
        form = SupplierForm()
    
    return render(request, 'suppliers/supplier_form.html', {
        'form': form,
        'title': 'Create Supplier'
    })


def supplier_detail(request, uid):
    """Display details of a specific supplier."""
    try:
        supplier = Supplier.nodes.get(uid=uid)
        # Get all products supplied by this supplier
        supplied_products = supplier.supplies.all()
        
        return render(request, 'suppliers/supplier_detail.html', {
            'supplier': supplier,
            'supplied_products': supplied_products
        })
    except Supplier.DoesNotExist:
        raise Http404("Supplier not found")


def supplier_edit(request, uid):
    """Edit an existing supplier."""
    try:
        supplier = Supplier.nodes.get(uid=uid)
    except Supplier.DoesNotExist:
        raise Http404("Supplier not found")
    
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            try:
                # Update supplier properties
                supplier.name = form.cleaned_data['name']
                supplier.contact_person = form.cleaned_data['contact_person']
                supplier.email = form.cleaned_data['email']
                supplier.phone = form.cleaned_data['phone']
                supplier.address = form.cleaned_data['address']
                supplier.country = form.cleaned_data['country']
                supplier.updated_at = datetime.now()
                supplier.save()
                
                messages.success(request, f'Supplier "{supplier.name}" updated successfully!')
                return redirect('supplier_detail', uid=uid)
            except Exception as e:
                messages.error(request, f'Error updating supplier: {str(e)}')
    else:
        # Pre-populate form with existing data
        form = SupplierForm(initial={
            'name': supplier.name,
            'contact_person': supplier.contact_person,
            'email': supplier.email,
            'phone': supplier.phone,
            'address': supplier.address,
            'country': supplier.country
        })
    
    return render(request, 'suppliers/supplier_form.html', {
        'form': form,
        'title': 'Edit Supplier',
        'supplier': supplier
    })


def supplier_delete(request, uid):
    """Delete a supplier."""
    try:
        supplier = Supplier.nodes.get(uid=uid)
        supplier_name = supplier.name
        supplier.delete()
        messages.success(request, f'Supplier "{supplier_name}" deleted successfully!')
    except Supplier.DoesNotExist:
        messages.error(request, 'Supplier not found')
    except Exception as e:
        messages.error(request, f'Error deleting supplier: {str(e)}')
    
    return redirect('supplier_list')


# ==================== PRODUCT VIEWS ====================

def product_list(request):
    """Display list of all products."""
    products = Product.nodes.all()
    return render(request, 'suppliers/product_list.html', {
        'products': products
    })


def product_create(request):
    """Create a new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                # Create product node
                product = Product(
                    name=form.cleaned_data['name'],
                    sku=form.cleaned_data['sku'],
                    description=form.cleaned_data['description'],
                    category=form.cleaned_data['category'],
                    unit_of_measure=form.cleaned_data['unit_of_measure']
                ).save()
                
                messages.success(request, f'Product "{product.name}" created successfully!')
                return redirect('product_list')
            except Exception as e:
                messages.error(request, f'Error creating product: {str(e)}')
    else:
        form = ProductForm()
    
    return render(request, 'suppliers/product_form.html', {
        'form': form,
        'title': 'Create Product'
    })


def product_detail(request, uid):
    """Display details of a specific product."""
    try:
        product = Product.nodes.get(uid=uid)
        # Get all suppliers for this product
        suppliers = product.supplied_by.all()
        
        return render(request, 'suppliers/product_detail.html', {
            'product': product,
            'suppliers': suppliers
        })
    except Product.DoesNotExist:
        raise Http404("Product not found")


def product_edit(request, uid):
    """Edit an existing product."""
    try:
        product = Product.nodes.get(uid=uid)
    except Product.DoesNotExist:
        raise Http404("Product not found")
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                # Update product properties
                product.name = form.cleaned_data['name']
                product.sku = form.cleaned_data['sku']
                product.description = form.cleaned_data['description']
                product.category = form.cleaned_data['category']
                product.unit_of_measure = form.cleaned_data['unit_of_measure']
                product.updated_at = datetime.now()
                product.save()
                
                messages.success(request, f'Product "{product.name}" updated successfully!')
                return redirect('product_detail', uid=uid)
            except Exception as e:
                messages.error(request, f'Error updating product: {str(e)}')
    else:
        # Pre-populate form with existing data
        form = ProductForm(initial={
            'name': product.name,
            'sku': product.sku,
            'description': product.description,
            'category': product.category,
            'unit_of_measure': product.unit_of_measure
        })
    
    return render(request, 'suppliers/product_form.html', {
        'form': form,
        'title': 'Edit Product',
        'product': product
    })


def product_delete(request, uid):
    """Delete a product."""
    try:
        product = Product.nodes.get(uid=uid)
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
    except Exception as e:
        messages.error(request, f'Error deleting product: {str(e)}')
    
    return redirect('product_list')


# ==================== RELATIONSHIP VIEWS ====================

def link_supplier_product(request):
    """Link a supplier to a product (create SUPPLIES relationship)."""
    if request.method == 'POST':
        form = LinkSupplierProductForm(request.POST)
        if form.is_valid():
            try:
                supplier_uid = form.cleaned_data['supplier_uid']
                product_uid = form.cleaned_data['product_uid']
                unit_price = form.cleaned_data.get('unit_price')
                lead_time_days = form.cleaned_data.get('lead_time_days')
                
                # Get nodes
                supplier = Supplier.nodes.get(uid=supplier_uid)
                product = Product.nodes.get(uid=product_uid)
                
                # Create relationship
                rel_props = {}
                if unit_price is not None:
                    rel_props['unit_price'] = unit_price
                if lead_time_days is not None:
                    rel_props['lead_time_days'] = lead_time_days
                
                supplier.supplies.connect(product, rel_props)
                
                messages.success(request, f'Successfully linked "{supplier.name}" to "{product.name}"!')
                return redirect('supplier_detail', uid=supplier_uid)
            except Supplier.DoesNotExist:
                messages.error(request, 'Supplier not found')
            except Product.DoesNotExist:
                messages.error(request, 'Product not found')
            except Exception as e:
                messages.error(request, f'Error linking supplier to product: {str(e)}')
    else:
        form = LinkSupplierProductForm()
    
    return render(request, 'suppliers/link_supplier_product.html', {
        'form': form,
        'title': 'Link Supplier to Product'
    })


# ==================== STORE VIEWS ====================

def store_list(request):
    """Display list of all stores."""
    stores = Store.nodes.all()
    return render(request, 'suppliers/store_list.html', {
        'stores': stores
    })


def store_create(request):
    """Create a new store."""
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            try:
                # Create store node
                store = Store(
                    name=form.cleaned_data['name'],
                    location=form.cleaned_data['location'],
                    store_type=form.cleaned_data['store_type']
                ).save()
                
                messages.success(request, f'Store "{store.name}" created successfully!')
                return redirect('store_list')
            except Exception as e:
                messages.error(request, f'Error creating store: {str(e)}')
    else:
        form = StoreForm()
    
    return render(request, 'suppliers/store_form.html', {
        'form': form,
        'title': 'Create Store'
    })


def store_detail(request, uid):
    """Display details of a specific store."""
    try:
        store = Store.nodes.get(uid=uid)
        
        # Get all products available at this store with their quantities
        products_data = []
        for product in store.has_products.all():
            # Get relationship properties
            rel = store.has_products.relationship(product)
            products_data.append({
                'product': product,
                'quantity': rel.quantity,
                'aisle': rel.aisle,
                'last_updated': rel.last_updated
            })
        
        return render(request, 'suppliers/store_detail.html', {
            'store': store,
            'products_data': products_data
        })
    except Store.DoesNotExist:
        raise Http404('Store not found')


def store_edit(request, uid):
    """Edit an existing store."""
    try:
        store = Store.nodes.get(uid=uid)
        
        if request.method == 'POST':
            form = StoreForm(request.POST)
            if form.is_valid():
                try:
                    store.name = form.cleaned_data['name']
                    store.location = form.cleaned_data['location']
                    store.store_type = form.cleaned_data['store_type']
                    store.updated_at = datetime.now()
                    store.save()
                    
                    messages.success(request, f'Store "{store.name}" updated successfully!')
                    return redirect('store_detail', uid=uid)
                except Exception as e:
                    messages.error(request, f'Error updating store: {str(e)}')
        else:
            # Prepopulate form with existing data
            form = StoreForm(initial={
                'name': store.name,
                'location': store.location,
                'store_type': store.store_type,
            })
        
        return render(request, 'suppliers/store_form.html', {
            'form': form,
            'title': 'Edit Store',
            'store': store
        })
    except Store.DoesNotExist:
        raise Http404('Store not found')


def store_delete(request, uid):
    """Delete a store."""
    try:
        store = Store.nodes.get(uid=uid)
        store_name = store.name
        store.delete()
        messages.success(request, f'Store "{store_name}" deleted successfully!')
    except Store.DoesNotExist:
        messages.error(request, 'Store not found')
    except Exception as e:
        messages.error(request, f'Error deleting store: {str(e)}')
    
    return redirect('store_list')


# ==================== STOCK MANAGEMENT VIEWS ====================

def stock_assignment(request):
    """Assign a product to a store (create AVAILABLE_AT relationship)."""
    if request.method == 'POST':
        form = StockAssignmentForm(request.POST)
        if form.is_valid():
            product_uid = form.cleaned_data['product_uid']
            store_uid = form.cleaned_data['store_uid']
            quantity = form.cleaned_data['quantity']
            aisle = form.cleaned_data['aisle']
            
            try:
                product = Product.nodes.get(uid=product_uid)
                store = Store.nodes.get(uid=store_uid)
                
                # Check if relationship already exists
                if product.available_at.is_connected(store):
                    # Update existing relationship
                    rel = product.available_at.relationship(store)
                    rel.quantity = quantity
                    if aisle:
                        rel.aisle = aisle
                    rel.last_updated = datetime.now()
                    rel.save()
                    messages.success(request, f'Updated stock: "{product.name}" at "{store.name}" - Quantity: {quantity}')
                else:
                    # Create new relationship
                    rel_props = {
                        'quantity': quantity,
                        'last_updated': datetime.now()
                    }
                    if aisle:
                        rel_props['aisle'] = aisle
                    
                    product.available_at.connect(store, rel_props)
                    messages.success(request, f'Successfully assigned "{product.name}" to "{store.name}" - Quantity: {quantity}')
                
                return redirect('store_detail', uid=store_uid)
            except Product.DoesNotExist:
                messages.error(request, 'Product not found')
            except Store.DoesNotExist:
                messages.error(request, 'Store not found')
            except Exception as e:
                messages.error(request, f'Error assigning stock: {str(e)}')
    else:
        form = StockAssignmentForm()
    
    return render(request, 'suppliers/stock_form.html', {
        'form': form,
        'title': 'Assign Product to Store'
    })


# ==================== ANALYTICS VIEWS ====================

def dashboard(request):
    """
    Dashboard showing products with low stock (quantity < 10).
    """
    # Cypher query to find all products with quantity < 10 at any store
    query = """
    MATCH (product:Product)-[rel:AVAILABLE_AT]->(store:Store)
    WHERE rel.quantity < 10
    RETURN product, store, rel.quantity as quantity, rel.aisle as aisle
    ORDER BY rel.quantity ASC
    """
    
    results, meta = db.cypher_query(query)
    
    # Process results
    low_stock_items = []
    for row in results:
        product_node = Product.inflate(row[0])
        store_node = Store.inflate(row[1])
        quantity = row[2]
        aisle = row[3] if row[3] else 'N/A'
        
        low_stock_items.append({
            'product': product_node,
            'store': store_node,
            'quantity': quantity,
            'aisle': aisle
        })
    
    # Get total counts for statistics
    total_products = len(Product.nodes.all())
    total_stores = len(Store.nodes.all())
    total_suppliers = len(Supplier.nodes.all())
    
    return render(request, 'suppliers/dashboard.html', {
        'low_stock_items': low_stock_items,
        'total_products': total_products,
        'total_stores': total_stores,
        'total_suppliers': total_suppliers,
        'low_stock_count': len(low_stock_items)
    })
