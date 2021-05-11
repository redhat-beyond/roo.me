from .forms import SeekerCreationForm
from django.urls import reverse
import pytest


@pytest.mark.parametrize(
    'city, start_date, min_rent, max_rent, num_of_roomates, num_of_rooms, about, validity',
    [
        ('city_model', '2021-2-2', 1000, 2000, 2, 2, 'about', True),
        ('city_model', '', 1000, 2000, 2, 2, 'about', False),
        ('city_model', '2021-2-2', None, 2000, 2, 2, 'about', False),
        ('city_model', '2021-2-2', 1000, None, 2, 2, 'about', False),
        ('city_model', '2021-2-2', 1000, 2000, None, 2, 'about', False),
        ('city_model', '2021-2-2', 1000, 2000, 2, None, 'about', False),
        ('city_model', '2021-2-2', 2000, 1000, 2, 2, 'about', False),
        ('city_model', '2021-2-2', 1000, 2000, 2, 2, '', True),
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


@pytest.mark.django_db
def test_valid_form_is_valid(valid_seeker_creation_form):
    assert valid_seeker_creation_form.is_valid


@pytest.mark.django_db
def test_fail_to_save_seeker_form_with_commit_true(valid_seeker_creation_form):
    with pytest.raises(ValueError):
        valid_seeker_creation_form.save(commit=True)


@pytest.mark.django_db
def test_register_apartment_view(client):
    url = reverse('register_seeker')
    response = client.get(url)
    assert response.status_code == 200
