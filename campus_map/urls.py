from django.urls import path
from . import views

urlpatterns = [
    path('', views.campus_map_view, name='campus_map'),
    path('bus/', views.bus_map_view, name='bus_map'),
]
