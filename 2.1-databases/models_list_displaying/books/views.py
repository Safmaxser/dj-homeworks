from datetime import datetime

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    books = Book.objects.all().order_by('pub_date')
    # paginator = Paginator(books)
    template = 'books/books_list.html'
    context = {
        'books': books,
    }
    return render(request, template, context)


def books_date(request, dt: datetime):
    books = Book.objects.all()
    books_set = {b.pub_date for b in books}
    books_list = sorted(list(books_set))
    current_num = books_list.index(dt.date())
    paginator = Paginator(books_list, 1)
    page = paginator.get_page(current_num+1)
    next_page = None
    previous_page = None
    if page.has_next():
        next_page = books_list[page.next_page_number()-1]
    if page.has_previous():
        previous_page = books_list[page.previous_page_number()-1]
    books = Book.objects.filter(pub_date=dt)
    template = 'books/books_list.html'
    context = {
        'books': books,
        'next_page': next_page,
        'previous_page': previous_page,
    }
    return render(request, template, context)
