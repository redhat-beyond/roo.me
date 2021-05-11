import pytest
from .models import Connection, ConnectionType
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError


@pytest.mark.django_db
def test_add_connection(sample_connection):
    assert sample_connection is not None
    assert sample_connection.seeker.base_user.email == "t1@m.com"
    assert sample_connection.apartment.owner.email == "t3@m.com"


@pytest.mark.django_db
def test_find_connection(sample_connection):
    temp_connection = Connection.objects.get(seeker=sample_connection.seeker, apartment=sample_connection.apartment)
    assert temp_connection == sample_connection


@pytest.mark.django_db
def test_invalid_users_connection(make_seeker):
    user1 = get_user_model().objects.create_user("t1@m.com", "test1", "test", "1995-05-05", "testing")
    seeker1 = make_seeker(user1, "2020-05-05", 100, 1000, 2, 2, "Hello")
    user2 = get_user_model().objects.create_user("t2@m.com", "test2", "test", "1995-05-05", "testing")
    seeker2 = make_seeker(user2, "2020-05-05", 300, 3000, 3, 3, "Hi")
    with pytest.raises(ValueError):
        with transaction.atomic():
            Connection(seeker=seeker1, apartment=seeker2).save()


@pytest.mark.django_db
def test_invalid_duplicate_connection(sample_connection):
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Connection(seeker=sample_connection.seeker, apartment=sample_connection.apartment).save()


@pytest.mark.django_db
def test_multipile_connection(sample_connection, make_seeker):
    user2 = get_user_model().objects.create_user("t2@m.com", "test2", "test", "1995-05-05", "testing")
    seeker2 = make_seeker(user2, "2020-05-05", 300, 3000, 3, 3, "Hi")
    Connection(seeker=seeker2, apartment=sample_connection.apartment).save()
    amount = Connection.objects.filter(apartment=sample_connection.apartment).count()
    expected = 2
    assert amount == expected


@pytest.mark.django_db
def test_default_and_get_status_property(sample_connection):
    assert sample_connection.get_status == 'Pending'


@pytest.mark.django_db
def test_approve_pending_connection(sample_connection):
    assert sample_connection.get_status == 'Pending'
    sample_connection.approve()
    assert sample_connection.get_status == 'Approved'


@pytest.mark.django_db
def test_reject_pending_connection(sample_connection):
    assert sample_connection.get_status == 'Pending'
    sample_connection.reject()
    assert sample_connection.get_status == 'Rejected'


@pytest.mark.django_db
def test_approve_non_pending_connection(sample_connection):
    sample_connection.reject()
    with pytest.raises(ValueError):
        with transaction.atomic():
            sample_connection.approve()


@pytest.mark.django_db
def test_get_pending_connections(sample_connection):
    assert sample_connection.get_status == 'Pending'
    pendings = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.PENDING)
    assert pendings.count() == 1
    pendings = Connection.get_connections_by_user(sample_connection.apartment.owner, ConnectionType.PENDING)
    assert pendings.count() == 1
    assert pendings.first().seeker == sample_connection.seeker


@pytest.mark.django_db
def test_get_approved_connections(sample_connection):
    assert sample_connection.get_status == 'Pending'
    approved = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.APPROVED)
    assert approved.count() == 0
    sample_connection.approve()
    assert sample_connection.get_status == 'Approved'
    approved = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.APPROVED)
    assert approved.count() == 1


@pytest.mark.django_db
def test_seeker_redirect_to_contacts_page(sample_connection, client):
    seeker_email = "t1@m.com"
    seeker_pass = "testing"  # credentials for sample_connection.seeker
    client.login(email=seeker_email, password=seeker_pass)
    response = client.get('/contacts/')
    assert response.status_code == 200
    logged_user = response.wsgi_request.user
    assert logged_user == sample_connection.seeker.base_user
    assert b"This connection request has yet to be approved" in response.content


@pytest.mark.django_db
def test_owner_redirect_to_contacts_page(sample_connection, client):
    owner_email = "t3@m.com"
    owner_pass = "testing"  # credentials for sample_connection.apartment
    client.login(email=owner_email, password=owner_pass)
    response = client.get('/contacts/')
    assert response.status_code == 200
    logged_user = response.wsgi_request.user
    assert logged_user == sample_connection.apartment.owner
    assert b"You can approve or decline this connection" in response.content
