import pytest
from .models import Connection, ConnectionType, Message
from apartments.models import Apartment
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.contrib.messages import get_messages


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
def test_seeker_redirect_to_contacts_page(sample_connection, client, log_in_sample_connection_seeker):
    response = client.get('/contacts/')
    assert response.status_code == 200
    logged_user = response.wsgi_request.user
    assert logged_user == sample_connection.seeker.base_user
    assert b"This connection request has yet to be approved" in response.content


@pytest.mark.django_db
def test_owner_redirect_to_contacts_page(sample_connection, client, log_in_sample_connection_apartment):
    response = client.get('/contacts/')
    assert response.status_code == 200
    logged_user = response.wsgi_request.user
    assert logged_user == sample_connection.apartment.owner
    assert b"You can approve or decline this connection" in response.content


@pytest.mark.django_db
def test_seeker_add_contact(sample_connection, client, make_apartment, log_in_sample_connection_seeker):
    pendings = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.PENDING)
    assert pendings.count() == 1
    temp_user = get_user_model().objects.create_user("t4@m.com", "test4", "test", "1995-05-05", "testing")
    temp_apartment = make_apartment(temp_user, "Haickarim 5", 300, 3, 3, "2021-05-05")
    temp_id = temp_apartment.pk
    response = client.get(f'/contacts/add/{temp_id}', follow=True)
    assert response.status_code == 200
    pendings = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.PENDING)
    assert pendings.count() == 2
    ok_message = list(get_messages(response.wsgi_request))[0]
    assert ok_message.message == "Connection request sent!"


@pytest.mark.django_db
def test_owner_cant_add_contacts(client, log_in_sample_connection_apartment):
    response = client.get('/contacts/add/1', follow=True)
    assert response.status_code == 200
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "You can't send a connection request!"


@pytest.mark.django_db
def test_cant_add_unexisting_apartment(sample_connection, client, log_in_sample_connection_seeker):
    pendings = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.PENDING)
    assert pendings.count() == 1
    unexisting_id = (Apartment.objects.last().pk) + 1
    response = client.get(f'/contacts/add/{unexisting_id}', follow=True)
    assert response.status_code == 200
    pendings = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.PENDING)
    assert pendings.count() == 1
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "Invalid apartment request!"


@pytest.mark.django_db
def test_cant_add_duplicate_connection(sample_connection, client, log_in_sample_connection_seeker):
    pendings = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.PENDING)
    assert pendings.count() == 1
    curr_apartment = sample_connection.apartment
    curr_id = curr_apartment.pk
    response = client.get(f'/contacts/add/{curr_id}', follow=True)
    assert response.status_code == 200
    pendings = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.PENDING)
    assert pendings.count() == 1
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "You have already sent a connection request to this user!"


@pytest.mark.django_db
def test_approve_connection_url(sample_connection, client, log_in_sample_connection_apartment):
    assert sample_connection.status == 'P'  # pending
    approved = Connection.get_connections_by_user(sample_connection.apartment.owner, ConnectionType.APPROVED)
    assert approved.count() == 0
    response = client.get('/contacts/')
    assert response.wsgi_request.user == sample_connection.apartment.owner
    connection_id = sample_connection.id
    response = client.get(f'/contacts/approve/{connection_id}', follow=True)
    assert response.status_code == 200
    sample_connection.refresh_from_db()
    approved = Connection.get_connections_by_user(sample_connection.apartment.owner, ConnectionType.APPROVED)
    assert approved.count() == 1
    assert sample_connection.status == 'A'  # approved
    connection_seeker = sample_connection.seeker.base_user
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == f"You can now contact {connection_seeker.first_name}!"


@pytest.mark.django_db
def test_reject_connection_url(sample_connection, client, log_in_sample_connection_apartment):
    assert sample_connection.status == 'P'  # pending
    rejected = Connection.get_connections_by_user(sample_connection.apartment.owner, ConnectionType.REJECTED)
    assert rejected.count() == 0
    connection_id = sample_connection.id
    response = client.get(f'/contacts/reject/{connection_id}', follow=True)
    assert response.status_code == 200
    sample_connection.refresh_from_db()
    rejected = Connection.get_connections_by_user(sample_connection.apartment.owner, ConnectionType.REJECTED)
    assert rejected.count() == 1
    assert sample_connection.status == 'R'  # rejected
    connection_seeker = sample_connection.seeker.base_user
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == f"{connection_seeker.first_name} won't bother you anymore!"


@pytest.mark.django_db
def test_cant_use_unexisting_connection(sample_connection, client, log_in_sample_connection_apartment):
    approved = Connection.get_connections_by_user(sample_connection.apartment.owner, ConnectionType.APPROVED)
    assert approved.count() == 0
    unexisting_id = Connection.objects.last().id + 1
    response = client.get(f'/contacts/approve/{unexisting_id}', follow=True)
    assert response.status_code == 200
    approved = Connection.get_connections_by_user(sample_connection.apartment.owner, ConnectionType.APPROVED)
    assert approved.count() == 0
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "Invalid connection request!"


@pytest.mark.django_db
def test_cant_approve_connection_as_seeker(sample_connection, client, log_in_sample_connection_seeker):
    assert sample_connection.get_status == 'Pending'
    approved = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.APPROVED)
    assert approved.count() == 0
    connection_id = sample_connection.id
    response = client.get(f'/contacts/approve/{connection_id}', follow=True)
    assert response.status_code == 200
    approved = Connection.get_connections_by_user(sample_connection.seeker.base_user, ConnectionType.APPROVED)
    assert approved.count() == 0
    assert sample_connection.get_status == 'Pending'
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "You are not allowed to take action on this connection!"


@pytest.mark.django_db
def test_cant_approve_connection_as_other_owner(sample_connection, client, make_apartment):
    assert sample_connection.get_status == 'Pending'
    temp_user = get_user_model().objects.create_user("t6@m.com", "test6", "test", "1995-05-05", "testing")
    make_apartment(temp_user, "Haickarim 6", 300, 3, 3, "2021-05-05")
    owner_email = "t6@m.com"
    owner_pass = "testing"  # credentials for temp_user
    client.login(email=owner_email, password=owner_pass)
    connection_id = sample_connection.id
    response = client.get(f'/contacts/approve/{connection_id}', follow=True)
    assert response.wsgi_request.user != sample_connection.apartment.owner
    assert response.status_code == 200
    assert sample_connection.get_status == 'Pending'
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "You are not allowed to take action on this connection!"


@pytest.mark.django_db
def test_cant_approve_not_pending_connection(sample_connection, client, log_in_sample_connection_apartment):
    sample_connection.approve()
    assert sample_connection.get_status == 'Approved'
    approved = Connection.get_connections_by_user(sample_connection.apartment.owner, ConnectionType.APPROVED)
    assert approved.count() == 1
    connection_id = sample_connection.id
    response = client.get(f'/contacts/approve/{connection_id}', follow=True)
    assert response.status_code == 200
    approved = Connection.get_connections_by_user(sample_connection.apartment.owner, ConnectionType.APPROVED)
    assert approved.count() == 1
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "Can't approve this connection!"
    sample_connection.reject()
    assert sample_connection.get_status == 'Rejected'
    response = client.get(f'/contacts/approve/{connection_id}', follow=True)
    assert response.status_code == 200
    assert sample_connection.get_status == 'Rejected'
    approved = Connection.get_connections_by_user(sample_connection.apartment.owner, ConnectionType.APPROVED)
    assert approved.count() == 0
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "Can't approve this connection!"


@pytest.mark.django_db
def test_unvalid_action_on_connection(sample_connection, client, log_in_sample_connection_apartment):
    assert sample_connection.get_status == 'Pending'
    connection_id = sample_connection.id
    response = client.get(f'/contacts/rebase/{connection_id}', follow=True)
    assert response.status_code == 200
    assert sample_connection.get_status == 'Pending'
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "Invalid connection action!"


@pytest.mark.django_db
def test_get_chat_messages(sample_connection):
    assert sample_connection.get_chat_messages().count() == 0
    seeker_user = sample_connection.seeker.base_user
    owner_user = sample_connection.apartment.owner
    msg = Message(connection=sample_connection, author=seeker_user, text="hi")
    msg.save()
    msg = Message(connection=sample_connection, author=owner_user, text="hello")
    msg.save()
    assert sample_connection.get_chat_messages().count() == 2
    assert sample_connection.get_chat_messages().last().text == "hello"


@pytest.mark.django_db
def test_chat_page_validity(sample_connection, client, log_in_sample_connection_apartment):
    sample_connection.approve()
    connection_id = sample_connection.id
    response = client.get(f'/contacts/chat/{connection_id}')
    assert response.status_code == 200
    assert b"Recent Chats" in response.content


@pytest.mark.django_db
def test_cant_chat_unexisting_connection(client, log_in_sample_connection_apartment):
    unexisting_id = Connection.objects.last().id + 1
    response = client.get(f'/contacts/chat/{unexisting_id}', follow=True)
    assert response.status_code == 200
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "Invalid request!"


@pytest.mark.django_db
def test_cant_chat_without_connection(sample_connection, client, make_apartment):
    sample_connection.approve()
    temp_user = get_user_model().objects.create_user("t7@m.com", "test7", "test", "1995-05-05", "testing")
    make_apartment(temp_user, "Haickarim 6", 300, 3, 3, "2021-05-05")
    owner_email = "t7@m.com"
    owner_pass = "testing"  # credentials for temp_user
    client.login(email=owner_email, password=owner_pass)
    connection_id = sample_connection.id
    response = client.get(f'/contacts/chat/{connection_id}', follow=True)
    assert response.wsgi_request.user != sample_connection.apartment.owner
    assert response.status_code == 200
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "You are not allowed to enter this chat!"


@pytest.mark.django_db
def test_cant_chat_not_approved_connection(sample_connection, client, log_in_sample_connection_apartment):
    assert sample_connection.get_status == 'Pending'
    connection_id = sample_connection.id
    response = client.get(f'/contacts/chat/{connection_id}', follow=True)
    assert response.status_code == 200
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "This chat is yet to be approved!"


@pytest.mark.django_db
def test_send_new_message(sample_connection, client, log_in_sample_connection_apartment):
    sample_connection.approve()
    assert sample_connection.get_chat_messages().count() == 0
    connection_id = sample_connection.id
    response = client.get(f'/contacts/chat/{connection_id}', follow=True)
    msg = {'msg_sent': "Hello!"}
    response = client.post(f'/contacts/chat/{connection_id}', msg, follow=True)
    assert response.status_code == 200
    assert sample_connection.get_chat_messages().count() == 1
    assert sample_connection.get_chat_messages().last().text == "Hello!"


@pytest.mark.django_db
def test_cant_send_empty_message(sample_connection, client, log_in_sample_connection_apartment):
    sample_connection.approve()
    assert sample_connection.get_chat_messages().count() == 0
    connection_id = sample_connection.id
    response = client.get(f'/contacts/chat/{connection_id}', follow=True)
    msg = {'msg_sent': ""}
    response = client.post(f'/contacts/chat/{connection_id}', msg, follow=True)
    assert response.status_code == 200
    assert sample_connection.get_chat_messages().count() == 0
    error_message = list(get_messages(response.wsgi_request))[0]
    assert error_message.message == "Your message was empty!"
