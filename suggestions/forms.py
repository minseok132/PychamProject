from django import forms
from .models import Comment, Suggestion

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['title', 'content', 'attachment']
