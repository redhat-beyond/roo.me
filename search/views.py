from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from contacts.models import Connection
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .forms import PreferencesSearchForm
from apartments.models import Apartment, City
from datetime import datetime


@login_required
def search(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        preferences_form = PreferencesSearchForm(request.POST)
        if search_form.is_valid() and preferences_form.is_valid():
            filtered_apartments = get_filtered_apartments(search_form, preferences_form, request.user)
            results = True
    else:
        filtered_apartments = None
        results = None
        if request.user.is_owner is True:
            if request.user.apartment.rent > 500:
                search_form = SearchForm(
                    instance=request.user.apartment,
                    initial={
                        'min_rent': request.user.apartment.rent - 500,
                        'max_rent': request.user.apartment.rent + 500}
                )
            else:
                search_form = SearchForm(
                    instance=request.user.apartment,
                    initial={
                        'min_rent': 1,
                        'max_rent': 500}
                )
        elif request.user.is_seeker is True:
            search_form = SearchForm(instance=request.user.seeker)
        else:
            search_form = SearchForm({
                'city': City.objects.get(cityName='Tel Aviv'),
                'start_date': datetime.now(),
                'min_rent': 2000,
                'max_rent': 3000,
                'num_of_roomates': 2,
                'num_of_rooms': 3
            })

        preferences_form = PreferencesSearchForm(
            instance=request.user
        )

    context = {
        'search_form': search_form,
        'preferences_form': preferences_form,
        'loggedUser': request.user,
        'filteredApartments': filtered_apartments,
        'showResults': results
    }
    return render(request, 'search/search.html', context)


def get_filtered_apartments(search_form, preferences_form, user):
    filter_args = {
            'is_relevant': True,
            'start_date__lte': search_form['start_date'].value(),
            'city': search_form['city'].value(),
            'rent__gte': search_form['min_rent'].value(),
            'rent__lte': search_form['max_rent'].value(),
            'num_of_roomates': search_form['num_of_roomates'].value(),
            'num_of_rooms': search_form['num_of_rooms'].value()
        }

    if preferences_form['not_smoking'].value():
        filter_args['owner__not_smoking'] = True
    if preferences_form['pets_allowed'].value():
        filter_args['owner__pets_allowed'] = True
    if preferences_form['air_conditioner'].value():
        filter_args['owner__air_conditioner'] = True
    if preferences_form['balcony'].value():
        filter_args['owner__balcony'] = True
    if preferences_form['elevator'].value():
        filter_args['owner__elevator'] = True
    if preferences_form['long_term'].value():
        filter_args['ownner__long_term'] = True
    if preferences_form['immediate_entry'].value():
        filter_args['owner__immediate_entry'] = True

    relevant_apartments = Apartment.objects.filter(**filter_args)

    if user.is_seeker:
        for apartment in relevant_apartments:
            try:
                Connection.objects.get(seeker=user.seeker, apartment=apartment)
                relevant_apartments = relevant_apartments.exclude(pk=apartment.pk)
            except ObjectDoesNotExist:
                pass

    return relevant_apartments
