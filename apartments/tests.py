from users.models import User
from apartments.models import Apartment, City
import pytest


@pytest.mark.django_db
class TestModels:

    @pytest.fixture
    def new_user(self):
        user = User(
            email='test@test.com',
            first_name='first_name',
            last_name='last_name',
            birth_date='1900-01-01',
            password='password'
            )
        user.save()
        return user

    @pytest.fixture
    def new_city(self):
        city = City(cityName='some_city')
        city.save()
        return city

    @pytest.fixture
    def new_apartment(self, new_user, new_city):
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
