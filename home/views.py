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
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'DC': 'District of Columbia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'PR': 'Puerto Rico',
    'VI': 'Virgin Islands',
    'GU': 'Guam',
    'AS': 'American Samoa',
    'MP': 'Northern Mariana Islands',
    'FM': 'Micronesia',
    'MH': 'Marshall Islands',
    'PW': 'Palau',
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