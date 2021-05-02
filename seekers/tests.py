from apartments.models import City
from .forms import SeekerCreationForm
from django.urls import reverse
import pytest


@pytest.fixture
def new_city():
    city = City(cityName='some_city')
    city.save()
    return city


@pytest.mark.parametrize(
    'city, start_date, min_rent, max_rent, num_of_roomates, num_of_rooms, about, validity',
    [
        ('new_city', '2021-2-2', 1000, 2000, 2, 2, 'about', True),
        ('new_city', '', 1000, 2000, 2, 2, 'about', False),
        ('new_city', '2021-2-2', None, 2000, 2, 2, 'about', False),
        ('new_city', '2021-2-2', 1000, None, 2, 2, 'about', False),
        ('new_city', '2021-2-2', 1000, 2000, None, 2, 'about', False),
        ('new_city', '2021-2-2', 1000, 2000, 2, None, 'about', False),
        ('new_city', '2021-2-2', 2000, 1000, 2, 2, 'about', False),
        ('new_city', '2021-2-2', 1000, 2000, 2, 2, '', True),
    ])
@pytest.mark.django_db
def test_seeker_form_validity(city, start_date, min_rent, max_rent, num_of_roomates, num_of_rooms, about,
                              validity, request):

    city = request.getfixturevalue(city)
    form = SeekerCreationForm(data={
        'city': city,
        'start_date': start_date,
        'min_rent': min_rent,
        'max_rent': max_rent,
        'num_of_roomates': num_of_roomates,
        'num_of_rooms': num_of_rooms,
        'about': about,
    })

    assert form.is_valid() is validity


@pytest.fixture
def valid_form(new_city):
    return SeekerCreationForm(data={
        'city': new_city,
        'start_date': '1900-1-1',
        'min_rent': 1000,
        'max_rent': 4000,
        'num_of_roomates': 2,
        'num_of_rooms': 3,
        'about': 'about',
    })


@pytest.mark.django_db
def test_valid_form_is_valid(valid_form):
    assert valid_form.is_valid


@pytest.mark.django_db
def test_fail_to_save_seeker_form_with_commit_true(valid_form):
    with pytest.raises(ValueError):
        valid_form.save(commit=True)


@pytest.mark.django_db
def test_register_apartment_view(client):
    url = reverse('register_seeker')
    response = client.get(url)
    assert response.status_code == 200
