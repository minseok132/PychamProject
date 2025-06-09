from django.urls import path
from .views import signup_view, profile_view, profile_edit_view, CustomLoginView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
