from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sor_request = request.GET.get('sort', None)
    sort = {'name': 'name', 'min_price': 'price', 'max_price': '-price'}.get(
        sor_request, None)
    if sort:
        phones = Phone.objects.all().order_by(sort)
    else:
        phones = Phone.objects.all()
    template = 'catalog.html'
    context = {
        'phones': phones,
    }
    return render(request, template, context)


def show_product(request, slug):
    phone = Phone.objects.get(slug=slug)
    print(phone)
    template = 'product.html'
    context = {
        'phone': phone,
    }
    return render(request, template, context)
