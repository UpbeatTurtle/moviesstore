from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse
from cart.models import Item
from django.shortcuts import render

def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {
        'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request,
                  'home/about.html',
                  {'template_data': template_data})


STATE_NAMES = {
    'AL': 'Alabama',
    'CA': 'California',
    'FL': 'Florida',
    'GA': 'Georgia',
    'NY': 'New York',
    'TX': 'Texas',
    # one line per state code you put in the cart dropdown
}

def map(request):
    template_data = {}
    template_data['title'] = 'Map'
    return render(request, 'home/map.html',
                  {'template_data': template_data})

def map_data(request):
    rows = (
        Item.objects
        .exclude(order__region='')
        .values('order__region', 'movie__id', 'movie__name')
        .annotate(total=Sum('quantity'))
        .order_by('order__region', '-total')
    )
    best = {}
    for row in rows:
        code = row['order__region']
        if code in best:
            continue
        best[code] = {
            'code': code,
            'name': STATE_NAMES.get(code, code),
            'movie': row['movie__name'],
            'quantity': row['total'],
            'url': reverse('movies.show', args=[row['movie__id']]),
        }
    return JsonResponse({'regions': list(best.values())})