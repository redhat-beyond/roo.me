from django.db import migrations, transaction
from apartments.models import City
from users.recources.cities import CITIES_NAMES_LIST


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
        ('apartments', '0001_initial'),
    ]

    def generate_city_data(apps, schema_editor):
        with transaction.atomic():
            for name in CITIES_NAMES_LIST:
                City(cityName=name).save()

    operations = [
        migrations.RunPython(generate_city_data),
    ]
