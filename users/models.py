from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)
from roo_me.settings import AUTH_USER_MODEL


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


class Hobby(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    hobbies = models.ManyToManyField(Hobby)

    not_smoking = models.BooleanField(default=False, blank=True)
    pets_allowed = models.BooleanField(default=False, blank=True)
    air_conditioner = models.BooleanField(default=False, blank=True)
    balcony = models.BooleanField(default=False, blank=True)
    elevator = models.BooleanField(default=False, blank=True)
    long_term = models.BooleanField(default=False, blank=True)
    immediate_entry = models.BooleanField(default=False, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_date']

    def __str__(self):
        return self.email


class City(models.Model):
    cityName = models.CharField(max_length=100)

    def __str__(self):
        return self.cityName


class Apartment(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner_apartments')
    datePosted = models.DateTimeField(default=timezone.now, blank=True)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, related_name='city_apartments')
    address = models.TextField()
    rentPricePerMonth = models.IntegerField()
    numOfRoomates = models.IntegerField()
    numOfRooms = models.IntegerField()
    startDate = models.DateField()
    content = models.TextField(blank=True)
    isRelevant = models.BooleanField(default=True, blank=True)
    # img = models.ImageField(default='default.jpg', upload_to='aprt_pics')

    def __str__(self):
        return f"Owner:{self.owner}, Addres:{self.address}, City:{self.city}"
