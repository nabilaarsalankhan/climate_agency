"""
URL configuration for ecome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.urls import path
from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='climate_data_index'), 
    path('dashboard/', views.dashboard, name='dashboard'),   # Dashboard
    
    path('', include('climate_data.urls')),# 👈 replace 'yourappname' with your Django app name
    path('accounts/', include('accounts.urls')),  # Accounts
    path('dashboard/', include('dashboard.urls')),  # Dashboard
  
]
