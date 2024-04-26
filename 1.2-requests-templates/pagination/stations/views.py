import csv

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, newline='', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
    paginator = Paginator(reader, 10)
    current_page = int(request.GET.get('page', 1))
    stations = paginator.get_page(current_page)
    context = {
        'bus_stations': stations.object_list,
        'page': stations,
    }
    return render(request, 'stations/index.html', context)
