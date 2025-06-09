from django.urls import path
from . import views

app_name = 'calendar_app'
urlpatterns = [
    # 📅 메인 달력 페이지
    path('', views.calendar_view, name='calendar'),

    # AJAX: 공부 시간 추가/삭제
    path('api/add_worklog/', views.add_worklog, name='add_worklog'),
    path('api/delete_worklog/', views.delete_worklog, name='delete_worklog'),

    # AJAX: 메모 추가/삭제
    path('api/add_memo/', views.add_memo, name='add_memo'),
    path('api/delete_memo/', views.delete_memo, name='delete_memo'),

    # AJAX: 학식메뉴 텍스트/사진 저장
    path('api/add_menu_text/', views.add_menu_text, name='add_menu_text'),
    path('api/upload_menu_photo/', views.upload_menu_photo, name='upload_menu_photo'),

    # 메뉴 디테일 (업로드 후 달력으로 리다이렉트)
    path(
        'menu/<int:year>/<int:month>/<int:day>/',
        views.menu_detail,
        name='menu_detail'

    ),
    path('api/delete_menu_text/', views.delete_menu_text, name='delete_menu_text'),
    path('api/delete_menu_photo/', views.delete_menu_photo, name='delete_menu_photo'),

    # 📝 건의 작성 (폼에서 POST)
    path('submit_suggestion/', views.submit_suggestion, name='submit_suggestion'),

    # 📋 건의함 리스트 (calendar_app 내 간단 뷰)
    path('suggestions/', views.suggestion_community, name='suggestion_community'),
]
