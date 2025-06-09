from django.shortcuts import render
from .models import Suggestion

# Create your views here.
def suggestion_community(request):
    suggestions = Suggestion.objects.order_by('-created_at')
    return render(request, 'suggestion_box/suggestion_community.html', {
        'suggestions': suggestions,
    })