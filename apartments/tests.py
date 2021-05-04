from users.models import User
from apartments.models import Apartment, City
from .forms import ApartmentCreationForm
from django.urls import reverse
import pytest


@pytest.fixture
def new_user():
    user = User.objects.create_user(
        email='test@test.com',
        first_name='first_name',
        last_name='last_name',
        birth_date='1900-01-01',
        password='password'
    )
    user.save()
    return user


@pytest.fixture
def new_city():
    city = City(cityName='some_city')
    city.save()
    return city


@pytest.fixture
def new_apartment(new_user, new_city):
    apartment = Apartment(
        owner=new_user,
        city=new_city,
        address='street',
        rent=4500,
        num_of_roomates=2,
        num_of_rooms=3,
        start_date='2021-1-1',
        about='Hey!',
        image_url='www.some-url.com',
    )
    apartment.save()
    return apartment


@pytest.mark.django_db
class TestModels:

    def test_city_creation(self, new_city):
        assert new_city is not None
        assert new_city.cityName == 'some_city'

    def test_get_city(self, new_city):
        check_city = City.objects.get(cityName=new_city.cityName)
        assert check_city == new_city

    def test_apartment_creation(self, new_apartment):
        assert new_apartment is not None
        assert new_apartment.address == 'street'
        assert new_apartment.rent == 4500
        assert new_apartment.is_relevant is True

    def test_get_apartment(self, new_apartment):
        check_apartment = Apartment.objects.get(owner=new_apartment.owner)
        assert check_apartment == new_apartment

    def test_get_apartment_by_id(self, new_apartment):
        check_apartment_success = Apartment.get_apartment_by_id(new_apartment.owner.id)
        check_apartment_fail = Apartment.get_apartment_by_id(-1)
        assert check_apartment_success == new_apartment
        assert check_apartment_fail is None


@pytest.mark.django_db
class TestViews:

    def test_update_apartment_view_to_owner(self, client, new_apartment):
        client.login(email='test@test.com', password='password')
        response = client.get('/apartments/update')
        assert response.status_code == 200

    def test_update_apartment_view_to_not_owner_user(self, client, new_user):
        client.login(email='test@test.com', password='password')
        response = client.get('/apartments/update')
        assert response.status_code == 302
        response = client.get(response.url)
        assert response.status_code == 200


@pytest.mark.parametrize(
    'city, address, rent, num_of_roomates, num_of_rooms, start_date, about, validity',
    [
        ('new_city', 'address', 1000, 2, 2, '2021-2-2', 'about', True),
        ('new_city', '', 1000, 2, 2, '2021-2-2', 'about', False),
        ('new_city', 'address', None, 2, 2, '2021-2-2', 'about', False),
        ('new_city', 'address', 1000, None, 2, '2021-2-2', 'about', False),
        ('new_city', 'address', 1000, 2, None, '2021-2-2', 'about', False),
        ('new_city', 'address', 1000, 2, 2, '', 'about', False),
        ('new_city', 'address', 1000, 2, 2, '2021-2-2', '', True),
        ('new_city', 'address', -1, 2, 2, '2021-2-2', 'about', False),
        ('new_city', 'address', 1000, -1, 2, '2021-2-2', 'about', False),
        ('new_city', 'address', 1000, 2, -1, '2021-2-2', 'about', False),
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


@pytest.fixture
def valid_form(new_city):
    return ApartmentCreationForm(data={
        'city': new_city,
        'address': 'address',
        'rent': 10,
        'num_of_roomates': 2,
        'num_of_rooms': 2,
        'start_date': 2020-1-1,
        'about': 'about',
    })


@pytest.mark.django_db
def test_valid_form_is_valid(valid_form):
    assert valid_form.is_valid


@pytest.mark.django_db
def test_fail_to_save_apartment_form_with_commit_true(valid_form):
    with pytest.raises(ValueError):
        valid_form.save(commit=True)


@pytest.mark.django_db
def test_register_apartment_view(client):
    url = reverse('register_apartment')
    response = client.get(url)
    assert response.status_code == 200
