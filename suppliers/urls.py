"""
URL configuration for suppliers app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Supplier URLs
    path('', views.supplier_list, name='supplier_list'),
    path('create/', views.supplier_create, name='supplier_create'),
    
    # Product URLs (must come before <str:uid>/ to avoid conflicts)
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<str:uid>/', views.product_detail, name='product_detail'),
    path('products/<str:uid>/edit/', views.product_edit, name='product_edit'),
    path('products/<str:uid>/delete/', views.product_delete, name='product_delete'),
    
    # Relationship URLs (must come before <str:uid>/ to avoid conflicts)
    path('link/supplier-product/', views.link_supplier_product, name='link_supplier_product'),
    
    # Supplier detail URLs (must come LAST because <str:uid> catches everything)
    path('<str:uid>/', views.supplier_detail, name='supplier_detail'),
    path('<str:uid>/edit/', views.supplier_edit, name='supplier_edit'),
    path('<str:uid>/delete/', views.supplier_delete, name='supplier_delete'),
]
