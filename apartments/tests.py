from apartments.models import Apartment
from .forms import ApartmentCreationForm
from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestModels:

    def test_city_creation(self, city_model):
        assert city_model.cityName == 'nice_city'

    def test_apartment_creation(self, apartment_model):
        assert apartment_model.address == 'street'
        assert apartment_model.rent == 4500
        assert apartment_model.is_relevant

    def test_get_apartment_by_id(self, apartment_model):
        check_apartment_success = Apartment.get_apartment_by_id(apartment_model.owner.id)
        check_apartment_fail = Apartment.get_apartment_by_id(-1)
        assert check_apartment_success == apartment_model
        assert check_apartment_fail is None

    def test_get_all_relevant_apartments(self):
        apartments_qurey = Apartment.get_all_relevant_apartments()
        assert all(isinstance(current_apartment, Apartment) for current_apartment in apartments_qurey)
        assert all(current_apartment.is_relevant for current_apartment in apartments_qurey)


@pytest.mark.django_db
class TestViews:

    def test_update_apartment_view_to_owner(self, client, apartment_model):
        client.login(email='apartmentemail@address.com', password='password')
        response = client.get('/apartments/update')
        assert response.status_code == 200

    def test_update_apartment_view_to_not_owner_user(self, client, user_model):
        client.login(email='email@address.com', password='password')
        response = client.get('/apartments/update')
        assert response.status_code == 302
        response = client.get(response.url)
        assert response.status_code == 200


@pytest.mark.parametrize(
    'city, address, rent, num_of_roomates, num_of_rooms, start_date, about, validity',
    [
        ('city_model', 'address', 1000, 2, 2, '2021-2-2', 'about', True),
        ('city_model', '', 1000, 2, 2, '2021-2-2', 'about', False),
        ('city_model', 'address', None, 2, 2, '2021-2-2', 'about', False),
        ('city_model', 'address', 1000, None, 2, '2021-2-2', 'about', False),
        ('city_model', 'address', 1000, 2, None, '2021-2-2', 'about', False),
        ('city_model', 'address', 1000, 2, 2, '', 'about', False),
        ('city_model', 'address', 1000, 2, 2, '2021-2-2', '', True),
        ('city_model', 'address', -1, 2, 2, '2021-2-2', 'about', False),
        ('city_model', 'address', 1000, -1, 2, '2021-2-2', 'about', False),
        ('city_model', 'address', 1000, 2, -1, '2021-2-2', 'about', False),
    ])
@pytest.mark.django_db
def test_apartment_form_validity(city, address, rent, num_of_roomates, num_of_rooms, start_date, about,
                                 validity, request):

    city = request.getfixturevalue(city)
    form = ApartmentCreationForm(data={
        'city': city,
        'address': address,
        'rent': rent,
        'num_of_roomates': num_of_roomates,
        'num_of_rooms': num_of_rooms,
        'start_date': start_date,
        'about': about,
    })

    assert form.is_valid() is validity


@pytest.mark.django_db
def test_valid_form_is_valid(valid_apartment_creation_form):
    assert valid_apartment_creation_form.is_valid


@pytest.mark.django_db
def test_fail_to_save_apartment_form_with_commit_true(valid_apartment_creation_form):
    with pytest.raises(ValueError):
        valid_apartment_creation_form.save(commit=True)


@pytest.mark.django_db
def test_register_apartment_view(client):
    url = reverse('register_apartment')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_accessing_apartment_register_view_with_logged_user(client, user_model):
    client.login(email='email@address.com', password='password')
    url = reverse('register_apartment')
    response = client.get(url)
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 200
