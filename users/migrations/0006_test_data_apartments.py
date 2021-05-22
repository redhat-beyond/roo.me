from django.db import migrations, transaction
from users.models import User
from apartments.models import Apartment, City
from users.recources.about_data import APARTMENT_ABOUT
from users.recources.streets import STREETS_LIST
from users.recources.images import APARTMENT_IMAGE_URL_LIST
import random


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_test_data_seekers'),
    ]

    def generate_apartment_data(apps, schema_editor):
        apt_test_data = [
            (User.objects.get(email='apartment_owner1@gmail.com'), City.objects.get(cityName='Tel Aviv'),
             'Israelof 5', 2650, 2, 3, '2020-01-01', "Join our cool aprt!"),
            (User.objects.get(email='apartment_owner2@gmail.com'), City.objects.get(cityName='Jerusalem'),
             'Yoseftal 6', 3200, 3, 4, '2020-02-02', "Good vibes only"),
        ]
        with transaction.atomic():
            for baseuser, city, address, rent, roomates, rooms, startdate, about in apt_test_data:
                Apartment(
                    owner=baseuser,
                    city=city,
                    address=address,
                    rent=rent,
                    num_of_roomates=roomates,
                    num_of_rooms=rooms,
                    start_date=startdate,
                    about=about,
                    image_url=random.choice(APARTMENT_IMAGE_URL_LIST)).save()

    def generate_more_apartment_data(apps, schema_editor):
        users = User.objects.all()[100:]
        cities = City.objects.all()

        with transaction.atomic():
            for user in users:
                start_date = "2021-" + str(random.randint(1, 12)) + \
                    "-" + str(random.randint(1, 28))
                address = random.choice(STREETS_LIST) + ", " + \
                    str(random.randint(1, 150))
                num_of_roomates = random.randint(2, 4)
                num_of_rooms = num_of_roomates + random.randint(0, 3)
                Apartment(
                    owner=user,
                    city=cities[random.randint(0, 9)],
                    address=address,
                    rent=random.randint(1500, 5000),
                    num_of_roomates=num_of_roomates,
                    num_of_rooms=num_of_rooms,
                    start_date=start_date,
                    about=random.choice(APARTMENT_ABOUT),
                    image_url=random.choice(APARTMENT_IMAGE_URL_LIST)).save()

    operations = [
        migrations.RunPython(generate_apartment_data),
        migrations.RunPython(generate_more_apartment_data),
    ]
