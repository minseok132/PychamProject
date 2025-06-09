from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),  # ✅ “내 채팅방 목록”으로 이동
    path('start/<str:username>/', views.start_chat, name='start_chat'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
]
