from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
import pytest


@pytest.fixture
def superuser_model():
    return get_user_model().objects.create_superuser(
        'email@address.com', 'first_name', 'last_name', '1900-01-01', 'password'
    )


@pytest.mark.django_db
def test_superuser_creation(superuser_model):
    assert superuser_model.email == 'email@address.com'
    assert superuser_model.first_name == 'first_name'
    assert superuser_model.last_name == 'last_name'
    assert superuser_model.birth_date == '1900-01-01'
    assert superuser_model.is_active
    assert superuser_model.is_staff
    assert superuser_model.is_superuser
    assert str(superuser_model) == 'email@address.com'


@pytest.mark.django_db
def test_superuser_unique_email(superuser_model):
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            get_user_model().objects.create_superuser(
                'email@address.com', 'first_name', 'last_name', '1900-01-01', 'password'
            )


@pytest.mark.parametrize(
    'is_superuser_flag, is_staff_flag',
    [
        (True, False),
        (False, True),
        (False, False),
    ],
)
@pytest.mark.django_db
def test_superuser_flags(is_superuser_flag, is_staff_flag):
    with pytest.raises(ValueError):
        with transaction.atomic():
            get_user_model().objects.create_superuser(
                'email@address.com', 'first_name', 'last_name', '1900-01-01', 'password',
                is_superuser=is_superuser_flag, is_staff=is_staff_flag,
            )


@pytest.fixture
def user_model():
    return get_user_model().objects.create_user(
        'email@address.com', 'first_name', 'last_name', '1900-01-01', 'password'
    )


@pytest.mark.django_db
def test_user_creation(user_model):
    assert user_model.email == 'email@address.com'
    assert user_model.first_name == 'first_name'
    assert user_model.last_name == 'last_name'
    assert user_model.birth_date == '1900-01-01'
    assert user_model.is_active
    assert not user_model.is_staff
    assert not user_model.is_superuser
    assert str(user_model) == 'email@address.com'


@pytest.mark.parametrize(
    'email_field, first_name_field, last_name_field, birth_day_field',
    [
        ('', 'first_name', 'last_name', '1900-01-01',),
        ('email@address_1.com', '', 'last_name', '1900-01-01',),
        ('email@address_1.com', 'first_name', '', '1900-01-01',),
        ('email@address_1.com', 'first_name', 'last_name', '',),
    ],
)
@pytest.mark.django_db
def test_user_blank_fields(email_field, first_name_field, last_name_field, birth_day_field):
    with pytest.raises(ValueError):
        with transaction.atomic():
            get_user_model().objects.create_user(
                email_field, first_name_field, last_name_field, birth_day_field, 'password'
            )
