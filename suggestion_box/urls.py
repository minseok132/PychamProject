from django.urls import path
from . import views

app_name = 'suggestion_box'
urlpatterns = [
    path('', views.suggestion_community, name='suggestion_community'),
]