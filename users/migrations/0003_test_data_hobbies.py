from django.db import migrations, transaction
from users.models import Hobby
from users.recources.hobbies import HOBBIES_LIST


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_test_data_cities'),
    ]

    def generate_hobby_data(apps, schema_editor):
        with transaction.atomic():
            for hob in HOBBIES_LIST:
                Hobby(name=hob).save()

    operations = [
        migrations.RunPython(generate_hobby_data),
    ]
