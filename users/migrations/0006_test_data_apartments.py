from django.db import migrations, transaction
from users.models import User
from apartments.models import Apartment, City


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
                    about=about).save()

    operations = [
        migrations.RunPython(generate_apartment_data),
    ]
