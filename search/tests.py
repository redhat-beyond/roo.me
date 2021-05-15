import pytest
from django.urls import reverse
from search.forms import SearchForm
from search.views import get_filtered_apartments


@pytest.mark.django_db
class TestViews:

    def test_search_view_as_owner(self, client, apartment_model):
        client.login(email='apartmentemail@address.com', password='password')
        url = reverse('search')
        response = client.get(url)
        assert response.status_code == 200
        assert b"Search for apartments now!" in response.content

    def test_search_view_as_seeker(self, client, seeker_model):
        client.login(email='seekeremail@address.com', password='password')
        url = reverse('search')
        response = client.get(url)
        assert response.status_code == 200
        assert b"Search for apartments now!" in response.content

    def test_search_view_not_logged_user(self, client):
        url = reverse('search')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.parametrize(
    'city, start_date, min_rent, max_rent, num_of_roomates, num_of_rooms, validity',
    [
        ('city_model', '2021-02-02', 2000, 3000, 2, 3, True),
        ('city_model', '', 2000, 3000, 2, 3, False),
        ('city_model', '2021-02-02', None, 3000, 2, 3, False),
        ('city_model', '2021-02-02', 2000, None, 2, 3, False),
        ('city_model', '2021-02-02', 2000, 3000, None, 3, False),
        ('city_model', '2021-02-02', 2000, 3000, 2, None, False),
        ('city_model', '2021-13-02', 2000, 3000, 2, 3, False),
        ('city_model', '2021-02-31', 2000, 3000, 2, 3, False),
        ('city_model', '2021-02-02', -2, 3000, 2, 3, False),
        ('city_model', '2021-02-02', 2000, -2, 2, 3, False),
        ('city_model', '2021-02-02', 2000, 3000, -2, 3, False),
        ('city_model', '2021-02-02', 2000, 3000, 2, -3, False),
    ])
@pytest.mark.django_db
def test_search_form_validity(city, start_date, min_rent, max_rent, num_of_roomates, num_of_rooms, validity, request):
    city = request.getfixturevalue(city)
    form = SearchForm(data={
        'city': city,
        'start_date': start_date,
        'min_rent': min_rent,
        'max_rent': max_rent,
        'num_of_roomates': num_of_roomates,
        'num_of_rooms': num_of_rooms,
    })
    assert form.is_valid() is validity


@pytest.mark.django_db
def test_valid_form_is_valid(valid_search_form):
    assert valid_search_form.is_valid()


@pytest.mark.django_db
def test_not_successful_get_filtered_apartments(client, valid_search_form):
    filtered_apartments = get_filtered_apartments(valid_search_form)
    result = filtered_apartments.count()
    expectedResult = 0
    assert result is expectedResult


@pytest.mark.django_db
def test_success_get_filtered_aparts(client, valid_search_form, apart_success_search):
    filtered_apartments = get_filtered_apartments(valid_search_form)
    result = filtered_apartments.count()
    expectedResult = 1
    assert result is expectedResult


@pytest.mark.django_db
def test_multiple_success_get_filtered_aparts(client, valid_search_form, apart_success_search, apart2_success_search):
    filtered_apartments = get_filtered_apartments(valid_search_form)
    result = filtered_apartments.count()
    expectedResult = 2
    assert result is expectedResult
