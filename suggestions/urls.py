from django.urls import path
from . import views

urlpatterns = [
    path('suggestions/', views.suggestion_community, name='suggestion_community'),
    path('submit/', views.submit_suggestion, name='submit_suggestion'),
    path('suggestions/<int:pk>/', views.suggestion_detail, name='suggestion_detail'),
    path('suggestions/<int:pk>/edit/', views.suggestion_edit, name='suggestion_edit'),
    path('suggestions/<int:pk>/delete/', views.suggestion_delete, name='suggestion_delete'),
    path('suggestions/<int:suggestion_id>/react/', views.react_suggestion, name='react_suggestion'),

]
