import pytest
from users.models import User


@pytest.fixture
def make_user():
    def _make_user(email, f_name, l_name, b_date, passw):
        user = User(
            email=email,
            first_name=f_name,
            last_name=l_name,
            birth_date=b_date,
        )
        user.set_password(passw)
        user.save()
        return user

    return _make_user


@pytest.mark.django_db
class TestViews:

    def test_home_view(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_register_view(self, client):
        response = client.get('/register/')
        assert response.status_code == 200

    def test_enter_login_page(self, client):
        response = client.get('/login/')
        assert response.status_code == 200

    def test_enter_logout_page(self, client):
        response = client.get('/logout/')
        assert response.status_code == 200

    def test_successful_login_and_logout(self, client, make_user):
        sample_user = make_user("test1@gmail.com", "testy", "test", "1995-05-05", "test123")
        client.login(email="test1@gmail.com", password="test123")
        response = client.get('/')
        assert response.status_code == 200
        logged_user = response.wsgi_request.user
        assert logged_user == sample_user
        client.logout()
        response = client.get('/')
        assert response.status_code == 200
        logged_user = response.wsgi_request.user
        assert not logged_user == sample_user

    def test_valid_login_info(self, client, make_user):
        sample_user = make_user("test1@gmail.com", "testy", "test", "1995-05-05", "test123")
        credentials = {'username': "test1@gmail.com", 'password': "test123"}
        response = client.post('/login/', credentials, follow=True)
        assert response.status_code == 200
        assert sample_user == response.wsgi_request.user

    def test_invalid_login_info(self, client, make_user):
        make_user("test1@gmail.com", "testy", "test", "1995-05-05", "test123")
        credentials = {'username': "test3@g.com", 'password': "t3"}
        response = client.post('/login/', credentials, follow=True)
        assert response.status_code == 200
        assert b"Please enter a correct email" in response.content

    def test_logout_link_functionality(self, client, make_user):
        sample_user = make_user("test1@gmail.com", "testy", "test", "1995-05-05", "test123")
        client.login(email="test1@gmail.com", password="test123")
        response = client.get('/logout/')
        logged_user = response.wsgi_request.user
        assert not logged_user == sample_user
