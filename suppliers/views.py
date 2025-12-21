"""
Views for Supplier and Product management.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from neomodel import db
from datetime import datetime

from .models import Supplier, Product
from .forms import SupplierForm, ProductForm, LinkSupplierProductForm


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
