
from django.shortcuts import render, get_object_or_404
from core.models import Book

def index_view(request):
    """View function for home page of site."""

    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'core/index.html', context)

def book_detail_view(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'core/book_detail.html', {'book': book})
