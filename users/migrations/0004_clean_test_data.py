from django.db import migrations
from users.models import User, Hobby
from seekers.models import Seeker
from apartments.models import Apartment, City


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_test_data_cities'),
    ]

    def delete_seekers_test_data(apps, schema_editor):
        Seeker.objects.all().delete()

    def delete_apartments_test_data(apps, schema_editor):
        Apartment.objects.all().delete()

    def delete_users_test_data(apps, schema_editor):
        User.objects.all().delete()

    def delete_cities_test_data(apps, schema_editor):
        City.objects.all().delete()

    def delete_hobbies_test_data(apps, schema_editor):
        Hobby.objects.all().delete()

    operations = [
        migrations.RunPython(delete_seekers_test_data),
        migrations.RunPython(delete_apartments_test_data),
        migrations.RunPython(delete_users_test_data),
        migrations.RunPython(delete_cities_test_data),
        migrations.RunPython(delete_hobbies_test_data),
    ]
