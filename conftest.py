from django.contrib.auth import get_user_model
from seekers.models import Seeker
from apartments.models import Apartment, City
from contacts.models import Connection
from seekers.forms import SeekerCreationForm
from apartments.forms import ApartmentCreationForm
import pytest


@pytest.fixture
def superuser_model(db):
    super_user = get_user_model().objects.create_superuser(
        'email@address.com', 'first_name', 'last_name', '1900-01-01', 'password'
    )
    return super_user


@pytest.fixture
def user_model(db):
    user = get_user_model().objects.create_user(
        'email@address.com', 'first_name', 'last_name', '1900-01-01', 'password'
    )
    return user


@pytest.fixture
def city_model(db):
    new_city = City(cityName='nice_city')
    new_city.save()
    return new_city


@pytest.fixture
def seeker_model(db, city_model):
    new_base_user = get_user_model().objects.create_user(
        'seekeremail@address.com', 'seeker', 'macseek', '1900-01-01', 'password'
    )
    new_base_user.save()
    new_seeker = Seeker(
        base_user=new_base_user,
        city=city_model,
        start_date='1900-01-01',
        min_rent=1,
        max_rent=1000,
        num_of_roomates=2,
        num_of_rooms=2,
        about='test-seeker'
    )
    new_seeker.save()
    return new_seeker


@pytest.fixture
def apartment_model(db, city_model):
    new_owner = get_user_model().objects.create_user(
        'apartmentemail@address.com', 'owner', 'own', '1900-01-01', 'password'
    )
    new_owner.save()
    new_apartment = Apartment(
        owner=new_owner,
        city=city_model,
        address='street',
        rent=4500,
        num_of_roomates=2,
        num_of_rooms=3,
        start_date='2021-1-1',
        about='Hey!',
        image_url='www.some-url.com',
    )
    new_apartment.save()
    return new_apartment


@pytest.fixture
def valid_seeker_creation_form(db, city_model):
    return SeekerCreationForm(data={
        'city': city_model,
        'start_date': '1900-1-1',
        'min_rent': 1000,
        'max_rent': 4000,
        'num_of_roomates': 2,
        'num_of_rooms': 3,
        'about': 'about',
    })


@pytest.fixture
def valid_apartment_creation_form(db, city_model):
    return ApartmentCreationForm(data={
        'city': city_model,
        'address': 'address',
        'rent': 10,
        'num_of_roomates': 2,
        'num_of_rooms': 2,
        'start_date': 2020-1-1,
        'about': 'about',
    })


@pytest.fixture
def make_seeker(city_model):
    def _make_seeker(user, s_date, min_r, max_r, roomates, rooms, about):
        seeker = Seeker(
            base_user=user,
            city=city_model,
            start_date=s_date,
            min_rent=min_r,
            max_rent=max_r,
            num_of_roomates=roomates,
            num_of_rooms=rooms,
            about=about
        )
        seeker.save()
        return seeker

    return _make_seeker


@pytest.fixture
def make_apartment(city_model):
    def _make_apartment(user, addr, rent, roomates, rooms, s_date):
        apartmant = Apartment(
            owner=user,
            city=city_model,
            address=addr,
            rent=rent,
            num_of_roomates=roomates,
            num_of_rooms=rooms,
            start_date=s_date
        )
        apartmant.save()
        return apartmant

    return _make_apartment


@pytest.fixture
def sample_connection(db, make_seeker, make_apartment):
    user1 = get_user_model().objects.create_user("t1@m.com", "test1", "test", "1995-05-05", "testing")
    seeker = make_seeker(user1, "2020-05-05", 100, 1000, 2, 2, "Hello")
    user2 = get_user_model().objects.create_user("t3@m.com", "test3", "test", "1995-05-05", "testing")
    apartment = make_apartment(user2, "Hatotahim 5", 2500, 2, 3, "2020-05-05")
    con = Connection(seeker=seeker, apartment=apartment)
    con.save()
    return con
