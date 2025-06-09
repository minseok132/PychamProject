# used_books/forms.py
from django import forms
from .models import UsedBook

class UsedBookForm(forms.ModelForm):
    class Meta:
        model = UsedBook
        fields = ['title', 'author', 'description', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300'
            }),
        }
