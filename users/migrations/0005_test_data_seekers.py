from django.db import migrations, transaction
from users.models import User
from seekers.models import Seeker
from apartments.models import City


class Migration(migrations.Migration):

    dependencies = [
        ('seekers', '0001_initial'),
        ('users', '0004_test_data_users'),
    ]

    def generate_seeker_data(apps, schema_editor):
        seekers_test_data = [
            (User.objects.get(email='seeker1@gmail.com'), City.objects.get(cityName='Tel Aviv'),
             '2020-01-01', 2500, 2800, 2, 3, "Hey I'm seeker1"),
            (User.objects.get(email='seeker2@gmail.com'), City.objects.get(cityName='Jerusalem'),
             '2020-02-02', 3000, 3300, 3, 4, "Hey I'm seeker2"),
        ]
        with transaction.atomic():
            for baseuser, city, startdate, minrent, maxrent, roomates, rooms, about in seekers_test_data:
                Seeker(
                    base_user=baseuser,
                    city=city,
                    start_date=startdate,
                    min_rent=minrent,
                    max_rent=maxrent,
                    num_of_roomates=roomates,
                    num_of_rooms=rooms,
                    about=about).save()

    operations = [
        migrations.RunPython(generate_seeker_data),
    ]
