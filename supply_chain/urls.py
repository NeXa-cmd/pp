"""
URL configuration for supply_chain project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/suppliers/', permanent=False)),
    path('suppliers/', include('suppliers.urls')),
]
