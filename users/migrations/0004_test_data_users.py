from django.db import migrations, transaction
from users.models import User, Hobby


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_test_data_hobbies'),
    ]

    def generate_user_data(apps, schema_editor):
        users_test_data = [
            ('seeker1@gmail.com', 'seeker', 'one', '1995-05-05', 'testuser'),
            ('seeker2@gmail.com', 'seeker', 'two', '1996-06-06', 'testuser'),
            ('apartment_owner1@gmail.com', 'apartment_owner', 'one', '1997-07-07', 'testuser'),
            ('apartment_owner2@gmail.com', 'apartment_owner', 'two', '1998-08-08', 'testuser'),
            ('Amit@gmail.com', 'Amit', 'Aharoni', '1994-01-01', 'testuser'),
            ('Nadav@gmail.com', 'Nadav', 'Suliman', '1994-01-01', 'testuser'),
            ('Tamir@gmail.com', 'Tamir', 'Houri', '1994-01-01', 'testuser'),
            ('Daniel@gmail.com', 'Daniel', 'Malky', '1994-01-01', 'testuser'),
            ('Micha@gmail.com', 'Micha', 'Levy', '1994-01-01', 'testuser'),
        ]
        with transaction.atomic():
            for email, fname, lname, bdate, passw in users_test_data:
                User(email=email, first_name=fname, last_name=lname, birth_date=bdate, password=passw).save()

    def add_user_hobbies(apps, schema_editor):
        users_test_data = [
            (['Reading', 'Movies']),
            (['Walking', 'Traveling']),
            (['Reading', 'Movies']),
            (['Walking', 'Traveling']),
            (['Sports fan', 'Solving problems']),
            (['Basketball', 'CTFs', 'Gaming']),
            (['Running', 'Watching Netflix']),
            (['Movies', 'Snooker']),
            (['Watching Netflix']),
        ]
        with transaction.atomic():
            index = 0
            for userhobbies in users_test_data:
                for hobby in userhobbies:
                    hobby = Hobby.objects.get(name=hobby)
                    User.objects.all()[index].hobbies.add(hobby)
            index = index + 1

    operations = [
        migrations.RunPython(generate_user_data),
        migrations.RunPython(add_user_hobbies),
    ]
