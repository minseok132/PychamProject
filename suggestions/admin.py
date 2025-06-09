from django.contrib import admin
from .models import Suggestion, Comment, Reaction

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'suggestion', 'author', 'created_at']

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'suggestion', 'user', 'type']
