from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 📅 메인 앱: calendar_app
    path('', include('calendar_app.urls')),

    # 👤 계정 관리
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # 💡 건의함 기능: suggestions 앱 (별도 경로로 분리)
    path('suggestions/', include('suggestions.urls')),

    path('used_books/', include('used_books.urls')),

    path('chat/', include('chat.urls', namespace='chat')),
    path('campus/', include('campus_map.urls')),
    path('suggestion_box/', include('suggestion_box.urls')),
]

# 📂 개발 중 미디어 파일 서빙 (DEBUG=True일 때만)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
