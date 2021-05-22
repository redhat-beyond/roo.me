from django.db import migrations, transaction
from users.models import User, Hobby
from users.recources.names import FIRST_NAME_LIST, LAST_NAME_LIST
from users.recources.images import PROFILE_IMAGE_URL_LIST
import random


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_test_data_hobbies'),
    ]

    def generate_user_data(apps, schema_editor):
        default_password = "12345678"

        users_test_data = [
            ('seeker1@gmail.com', 'seeker', 'one',
             '1995-05-05', default_password, random.choice(PROFILE_IMAGE_URL_LIST)),
            ('seeker2@gmail.com', 'seeker', 'two',
             '1996-06-06', default_password, random.choice(PROFILE_IMAGE_URL_LIST)),
            ('apartment_owner1@gmail.com', 'apartment_owner',
             'one', '1997-07-07', default_password, random.choice(PROFILE_IMAGE_URL_LIST)),
            ('apartment_owner2@gmail.com', 'apartment_owner',
             'two', '1998-08-08', default_password, random.choice(PROFILE_IMAGE_URL_LIST)),
            ('Amit@gmail.com', 'Amit', 'Aharoni',
             '1994-01-01', default_password, random.choice(PROFILE_IMAGE_URL_LIST)),
            ('Nadav@gmail.com', 'Nadav', 'Suliman',
             '1994-01-01', default_password, random.choice(PROFILE_IMAGE_URL_LIST)),
            ('Tamir@gmail.com', 'Tamir', 'Houri',
             '1994-01-01', default_password, random.choice(PROFILE_IMAGE_URL_LIST)),
            ('Daniel@gmail.com', 'Daniel', 'Malky',
             '1994-01-01', default_password, random.choice(PROFILE_IMAGE_URL_LIST)),
            ('Micha@gmail.com', 'Micha', 'Levy',
             '1994-01-01', default_password, random.choice(PROFILE_IMAGE_URL_LIST)),
        ]

        for i in range(4000):
            first_name = random.choice(FIRST_NAME_LIST)
            last_name = random.choice(LAST_NAME_LIST)
            email = first_name + last_name + str(i) + "@gmail.com"
            birth_date = str(random.randint(1980, 2000)) + "-" + \
                str(random.randint(1, 12)) + "-" + str(random.randint(1, 28))
            image_url = random.choice(PROFILE_IMAGE_URL_LIST)
            user_details = (email, first_name, last_name,
                            birth_date, default_password, image_url)
            users_test_data.append(user_details)

        with transaction.atomic():
            for email, fname, lname, bdate, passw, img_url in users_test_data:
                User(email=email, first_name=fname, last_name=lname,
                     birth_date=bdate, password=passw, image_url=img_url).save()

    def add_user_hobbies(apps, schema_editor):
        with transaction.atomic():
            hobbies = Hobby.objects.all()
            for user in User.objects.all():
                for i in range(4):
                    hobby = random.choice(hobbies)
                    user.hobbies.add(hobby)
                user.save()

    def add_user_preferences(apps, schema_editor):
        with transaction.atomic():
            users = User.objects.all()
            for index, user in enumerate(users):
                if index % 7 == 0:
                    user.immediate_entry = True
                elif index % 7 == 1:
                    user.not_smoking = True
                elif index % 7 == 2:
                    user.pets_allowed = True
                elif index % 7 == 3:
                    user.air_conditioner = True
                elif index % 7 == 4:
                    user.balcony = True
                elif index % 7 == 5:
                    user.elevator = True
                elif index % 7 == 6:
                    user.long_term = True
                user.save()

    operations = [
        migrations.RunPython(generate_user_data),
        migrations.RunPython(add_user_hobbies),
        migrations.RunPython(add_user_preferences),
    ]
