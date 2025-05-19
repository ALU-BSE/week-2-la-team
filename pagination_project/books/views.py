from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book
from django.db.models import Q

def book_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    books = books.order_by('title')

    per_page = request.GET.get('per_page', 5)
    try:
        per_page = int(per_page)
        if per_page not in [5, 10, 20]:
            per_page = 5
    except ValueError:
        per_page = 5

    paginator = Paginator(books, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'query': query,
    }
    return render(request, 'books/book_list.html', context)
