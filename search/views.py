from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from apartments.models import Apartment, City
from datetime import datetime


@login_required
def search(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            form = SearchForm(request.POST)
            filtered_apartments = get_filtered_apartments(form)
            results = True
    else:
        filtered_apartments = None
        results = None
        if request.user.is_owner is True:
            search_form = SearchForm(
                instance=request.user.apartment,
                initial={
                    'min_rent': request.user.apartment.rent - 500,
                    'max_rent': request.user.apartment.rent + 500}
            )
        elif request.user.is_seeker is True:
            search_form = SearchForm(instance=request.user.seeker)
        else:
            search_form = SearchForm({
                'city': City.objects.get(cityName='Tel Aviv'),
                'start_date': datetime.now(),
                'min_rent': 1000,
                'max_rent': 3000,
                'num_of_roomates': 3,
                'num_of_rooms': 4
            })
    context = {
        'searchForm': search_form,
        'loggedUser': request.user,
        'filteredApartments': filtered_apartments,
        'showResults': results
    }
    return render(request, 'search/search.html', context)


def get_filtered_apartments(form):
    return Apartment.objects.filter(**{
            'is_relevant': True,
            'start_date__lte': form['start_date'].value(),
            'city': form['city'].value(),
            'rent__gte': form['min_rent'].value(),
            'rent__lte': form['max_rent'].value(),
            'num_of_roomates': form['num_of_roomates'].value(),
            'num_of_rooms': form['num_of_rooms'].value()
        })
