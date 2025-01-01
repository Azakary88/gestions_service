"""
URL configuration for secretaire_gestion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, get_resolver

urlpatterns = [
    path('admin/', admin.site.urls),
    path('produits_services/', include('produits_services.urls')),
    path('transactions/', include('transactions.urls')),
    path('', include('home.urls')),
    path('clients/', include('clients.urls')),
]

print(get_resolver().reverse_dict)