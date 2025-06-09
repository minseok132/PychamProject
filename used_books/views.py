from django.shortcuts import render, get_object_or_404, redirect
from .models import UsedBook
from django.contrib.auth.decorators import login_required
from .forms import UsedBookForm
from django.core.paginator import Paginator

def book_list(request):
    sort = request.GET.get('sort', 'latest')

    if sort == 'oldest':
        books = UsedBook.objects.all().order_by('created_at')
    elif sort == 'price':
        books = UsedBook.objects.all().order_by('price')
    else:  # 최신순
        books = UsedBook.objects.all().order_by('-created_at')

    # ⭐ 페이지네이션: 12개씩
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'used_books/book_list.html', {
        'page_obj': page_obj,
        'current_sort': sort
    })



def book_detail(request, pk):
    book = get_object_or_404(UsedBook, pk=pk)
    return render(request, 'used_books/book_detail.html', {'book': book})

@login_required
def book_create(request):
    if request.method == 'POST':
        form = UsedBookForm(request.POST, request.FILES)  # 이미지 업로드 처리
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            return redirect('used_books:book_list')
    else:
        form = UsedBookForm()
    return render(request, 'used_books/book_form.html', {'form': form})

@login_required
def book_update(request, pk):
    book = get_object_or_404(UsedBook, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = UsedBookForm(request.POST, request.FILES, instance=book)  # 이미지 업로드 처리
        if form.is_valid():
            form.save()
            return redirect('used_books:book_detail', pk=book.pk)
    else:
        form = UsedBookForm(instance=book)
    return render(request, 'used_books/book_form.html', {'form': form})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(UsedBook, pk=pk, seller=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('used_books:book_list')
    return render(request, 'used_books/book_confirm_delete.html', {'book': book})
