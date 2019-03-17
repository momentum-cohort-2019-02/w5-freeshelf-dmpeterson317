from django.shortcuts import render, get_object_or_404
from core.models import Book, BookCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index_view(request):
    """View function for home page of site."""
    book_list = Book.objects.all()
    categories = BookCategory.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(book_list, 8)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books,
        'categories': categories,
    }
    return render(request, 'core/index.html', context)

def book_detail_view(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'core/book_detail.html', {'book': book})

def category_detail_view(request, slug):
    category = get_object_or_404(BookCategory, slug=slug)
    return render(request, 'core/category_detail.html', {'category': category})
    