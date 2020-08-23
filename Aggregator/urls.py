"""Aggregator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from search.views import (
    index,
    get_paytm_data,
    get_shopclues_data,
    get_tata_cliq,
    save_to_database
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('api/paytm/', get_paytm_data, name="paytm_api"),
    path('api/shopclues/', get_shopclues_data ,name="shopclues_api"),
    path('api/tatacliq/', get_tata_cliq ,name="tatacliq_api"),
    path('api/save/', save_to_database, name="db_save"),
]
