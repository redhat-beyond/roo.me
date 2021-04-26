# import pytest


class TestViews:

    def test_home_view(self, client):
        response = client.get('/')
        assert response.status_code == 200
