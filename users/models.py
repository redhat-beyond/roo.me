from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)


class UserManager(BaseUserManager):

    def create_user(self, email, first_name,
                    last_name, birth_date, password,
                    **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        if not first_name:
            raise ValueError('You must provide a first name')

        if not last_name:
            raise ValueError('You must provide a last name')

        if not birth_date:
            raise ValueError('You must provide a birth date')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, birth_date=birth_date,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name,
                         last_name, birth_date, password,
                         **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if not other_fields.get('is_staff'):
            raise ValueError('superuser must be assigned to is_staff=True')

        if not other_fields.get('is_superuser'):
            raise ValueError('superuser must be assigned to is_superuser=True')

        return self.create_user(email, first_name,
                                last_name, birth_date, password,
                                **other_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_date']

    def __str__(self):
        return self.email
