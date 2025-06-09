from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from .models import Suggestion, Comment, SuggestionReaction
from django.views.decorators.http import require_POST
from .forms import CommentForm, SuggestionForm
from django.db.models import Count, Q
from django.core.paginator import Paginator


@login_required
def suggestion_community(request):
    sort = request.GET.get('sort', 'latest')

    if sort == 'recommend':
        suggestions = Suggestion.objects.annotate(
            recommend_count=Count('suggestionreaction', filter=Q(suggestionreaction__is_like=True))
        ).order_by('-recommend_count', '-created_at')
    elif sort == 'oldest':
        suggestions = Suggestion.objects.annotate(
            recommend_count=Count('suggestionreaction', filter=Q(suggestionreaction__is_like=True))
        ).order_by('created_at')
    else:  # 최신순
        suggestions = Suggestion.objects.annotate(
            recommend_count=Count('suggestionreaction', filter=Q(suggestionreaction__is_like=True))
        ).order_by('-created_at')

    # ⭐ 페이지네이션 처리
    paginator = Paginator(suggestions, 6)  # 6개씩 보여주기
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'calendar_app/suggestions.html', {
        'page_obj': page_obj,
        'current_sort': sort
    })


@login_required
def submit_suggestion(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('suggestion')
        attachment = request.FILES.get('attachment')  # 이미지 처리 추가

        if title and content:
            Suggestion.objects.create(
                title=title,
                content=content,
                author=request.user,
                attachment=attachment  # 이미지 저장
            )
            return redirect('suggestion_community')

    return render(request, 'calendar_app/suggestion_form.html')



@login_required
def suggestion_detail(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    comments = Comment.objects.filter(suggestion=suggestion, parent__isnull=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.suggestion = suggestion
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            return redirect('suggestion_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'calendar_app/suggestion_detail.html', {
        'suggestion': suggestion,
        'comments': comments,
        'comment_form': form,
        'likes': SuggestionReaction.objects.filter(suggestion=suggestion, is_like=True).count(),
        'dislikes': SuggestionReaction.objects.filter(suggestion=suggestion, is_like=False).count()
    })


@login_required
def suggestion_edit(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    if request.user != suggestion.author:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == 'POST':
        form = SuggestionForm(request.POST, request.FILES, instance=suggestion)
        if form.is_valid():
            form.save()
            return redirect('suggestion_detail', pk=pk)
    else:
        form = SuggestionForm(instance=suggestion)

    return render(request, 'calendar_app/suggestion_form.html', {'form': form})


@login_required
def suggestion_delete(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    if request.user != suggestion.author:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == 'POST':
        suggestion.delete()
        return redirect('suggestion_community')  # 목록 페이지 등으로 이동

    return render(request, 'calendar_app/suggestion_confirm_delete.html', {'suggestion': suggestion})


@require_POST
def react_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    is_like = request.POST.get("reaction") == "like"
    reaction, created = SuggestionReaction.objects.get_or_create(
        user=request.user, suggestion=suggestion,
        defaults={'is_like': is_like}
    )
    if not created:
        if reaction.is_like == is_like:
            return JsonResponse({'status': 'duplicate'})
        else:
            reaction.is_like = is_like
            reaction.save()

    likes = SuggestionReaction.objects.filter(suggestion=suggestion, is_like=True).count()
    dislikes = SuggestionReaction.objects.filter(suggestion=suggestion, is_like=False).count()
    return JsonResponse({'status': 'ok', 'likes': likes, 'dislikes': dislikes})
