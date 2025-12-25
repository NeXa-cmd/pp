"""
Django forms for Suppliers and Products.
"""

from django import forms
from .models import Supplier, Product, Store


class SupplierForm(forms.Form):
    """Form for creating and editing Suppliers."""
    
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter supplier name'
        })
    )
    contact_person = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact person name'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'supplier@example.com'
        })
    )
    phone = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890'
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter full address'
        })
    )
    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter country'
        })
    )


class ProductForm(forms.Form):
    """Form for creating and editing Products."""
    
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter product name'
        })
    )
    sku = forms.CharField(
        max_length=100,
        required=True,
        label='SKU',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter unique SKU (e.g., PROD-001)'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter product description'
        })
    )
    category = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Electronics, Food, Raw Materials'
        })
    )
    unit_of_measure = forms.CharField(
        max_length=50,
        initial='pieces',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., pieces, kg, liters'
        })
    )


class LinkSupplierProductForm(forms.Form):
    """Form for linking a Supplier to a Product."""
    
    supplier_uid = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Supplier'
    )
    product_uid = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Product'
    )
    unit_price = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter unit price',
            'step': '0.01'
        })
    )
    lead_time_days = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter lead time in days'
        }),
        label='Lead Time (days)'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate supplier choices
        suppliers = Supplier.nodes.all()
        supplier_choices = [(s.uid, s.name) for s in suppliers]
        self.fields['supplier_uid'].widget.choices = [('', '--- Select Supplier ---')] + supplier_choices
        
        # Populate product choices
        products = Product.nodes.all()
        product_choices = [(p.uid, f"{p.name} ({p.sku})") for p in products]
        self.fields['product_uid'].widget.choices = [('', '--- Select Product ---')] + product_choices


class StoreForm(forms.Form):
    """Form for creating and editing Stores."""
    
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter store name'
        })
    )
    location = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter store location/address'
        })
    )
    store_type = forms.ChoiceField(
        choices=[
            ('Retail', 'Retail'),
            ('Warehouse', 'Warehouse'),
            ('Distribution Center', 'Distribution Center'),
            ('Outlet', 'Outlet'),
            ('Flagship', 'Flagship'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Store Type'
    )


class StockAssignmentForm(forms.Form):
    """Form for assigning a Product to a Store (creating AVAILABLE_AT relationship)."""
    
    product_uid = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Product'
    )
    store_uid = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Store'
    )
    quantity = forms.IntegerField(
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter quantity'
        })
    )
    aisle = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., A1, B3, Warehouse-Section-2'
        }),
        label='Aisle/Location'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate product choices
        products = Product.nodes.all()
        product_choices = [(p.uid, f"{p.name} ({p.sku})") for p in products]
        self.fields['product_uid'].widget.choices = [('', '--- Select Product ---')] + product_choices
        
        # Populate store choices
        stores = Store.nodes.all()
        store_choices = [(s.uid, f"{s.name} - {s.location}") for s in stores]
        self.fields['store_uid'].widget.choices = [('', '--- Select Store ---')] + store_choices
