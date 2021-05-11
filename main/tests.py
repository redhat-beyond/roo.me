import pytest
from django.contrib.auth import get_user_model


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

    def test_successful_login_and_logout(self, client):
        sample_user = get_user_model().objects.create_user("test1@gmail.com", "testy", "test", "1995-05-05", "test123")
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

    def test_valid_login_info(self, client):
        sample_user = get_user_model().objects.create_user("test1@gmail.com", "testy", "test", "1995-05-05", "test123")
        credentials = {'username': "test1@gmail.com", 'password': "test123"}
        response = client.post('/login/', credentials, follow=True)
        assert response.status_code == 200
        assert sample_user == response.wsgi_request.user

    def test_invalid_login_info(self, client):
        get_user_model().objects.create_user("test1@gmail.com", "testy", "test", "1995-05-05", "test123")
        credentials = {'username': "test3@g.com", 'password': "t3"}
        response = client.post('/login/', credentials, follow=True)
        assert response.status_code == 200
        assert b"Please enter a correct email" in response.content

    def test_logout_link_functionality(self, client):
        sample_user = get_user_model().objects.create_user("test1@gmail.com", "testy", "test", "1995-05-05", "test123")
        client.login(email="test1@gmail.com", password="test123")
        response = client.get('/logout/')
        logged_user = response.wsgi_request.user
        assert not logged_user == sample_user
