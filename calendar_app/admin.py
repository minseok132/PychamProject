from django.contrib import admin
from .models import WorkLog, Memo, Event, CafeteriaMenu, MenuPhoto

@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'hours_worked', 'note')
    list_filter = ('date',)

@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ('date', 'note')
    list_filter = ('date',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'title')
    list_filter = ('date',)

@admin.register(CafeteriaMenu)
class CafeteriaMenuAdmin(admin.ModelAdmin):
    list_display = ('date', 'menu_text')
    list_filter = ('date',)

@admin.register(MenuPhoto)
class MenuPhotoAdmin(admin.ModelAdmin):
    list_display = ('menu', 'uploaded_at')
    list_filter = ('menu__date',)
