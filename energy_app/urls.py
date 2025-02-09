from django.urls import path
from .views import fetch_and_store_data
from .views import sensor_data_api
from django.views.generic import TemplateView

urlpatterns = [
    path('fetch-store/', fetch_and_store_data, name='fetch_store'),
    path('api/sensor-data/', sensor_data_api, name='sensor_data_api'),
    
    # The dashboard view (using a template view as an example)
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
]
