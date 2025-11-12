from django.urls import path
from . import views
from django.urls import path
from .views import ClimateDataAPIView
from django.urls import include


urlpatterns = [
     path('', views.index, name='climate_data_index'), 
     # path('dashboard/', views.dashboard, name='dashboard'),
     path('api/climate/', ClimateDataAPIView.as_view(), name='climate-api'),
     path('auth/', include('accounts.urls')),  # JWT endpoints under /auth/
     path('', include('climate_data.urls')),
]

