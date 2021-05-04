from django.db import migrations, transaction
from users.models import User, Hobby
from seekers.models import Seeker
from apartments.models import Apartment, City


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
        ('contacts', '0002_auto_20210428_0914'),
    ]

    def generate_hobby_data(apps, schema_editor):
        hobby_test_data = [
            ('Dancing'),
            ('Cooking'),
            ('Phishing'),
            ('Coding'),
        ]
        with transaction.atomic():
            for hob in hobby_test_data:
                Hobby(name=hob).save()

    def generate_city_data(apps, schema_editor):
        city_test_data = [
            ('Ramat Gan'),
            ('Raanana'),
        ]
        with transaction.atomic():
            for name in city_test_data:
                City(cityName=name).save()

    def generate_user_data(apps, schema_editor):
        user_test_data = [
            ('user1@hmail.com', 'Avi', 'Avraham', '1995-05-05', 'test123'),
            ('user2@hmail.com', 'Israel', 'Israeli', '1996-06-06', 'test123'),
            ('user3@hmail.com', 'Yossi', 'Yosef', '1997-07-07', 'test123'),
        ]
        with transaction.atomic():
            for email, fname, lname, bdate, passw in user_test_data:
                User(email=email, first_name=fname, last_name=lname, birth_date=bdate, password=passw).save()

    def generate_apartment_data(apps, schema_editor):
        apt_test_data = [
            ('Israelof 5', 2500, 2, 3, '2021-04-04'),
            ('Yoseftal 5', 3000, 1, 2, '2021-04-21'),
        ]
        with transaction.atomic():
            currcity = City.objects.first()
            index = 0
            for addr, rent, roomates, rooms, sdate in apt_test_data:
                Apartment(
                    owner=User.objects.all()[index],
                    city=currcity,
                    address=addr,
                    rent=rent,
                    num_of_roomates=roomates,
                    num_of_rooms=rooms,
                    start_date=sdate).save()
                index = index+1

    def generate_seeker_data(apps, schema_editor):
        seeker_test_data = [
            ('2020-01-01', 2000, 3000, 2, 2, "hi"),
        ]
        with transaction.atomic():
            curruser = User.objects.last()
            currcity = City.objects.first()
            for sdate, minrent, maxrent, roomates, rooms, about in seeker_test_data:
                Seeker(
                    base_user=curruser,
                    city=currcity,
                    start_date=sdate,
                    min_rent=minrent,
                    max_rent=maxrent,
                    num_of_roomates=roomates,
                    num_of_rooms=rooms,
                    about=about).save()

    operations = [
        migrations.RunPython(generate_hobby_data),
        migrations.RunPython(generate_city_data),
        migrations.RunPython(generate_user_data),
        migrations.RunPython(generate_apartment_data),
        migrations.RunPython(generate_seeker_data),
        ]
