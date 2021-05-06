from django.db import migrations, transaction
from seekers.models import Seeker
from apartments.models import Apartment
from contacts.models import Connection


class Migration(migrations.Migration):
    dependencies = [
        ('contacts', '0005_clean_test_data'),
        ('users', '0009_test_data_apartments'),
    ]

    def generate_connection_data(apps, schema_editor):
        connection_test_data = [
            (Seeker.objects.get(base_user__email='seeker1@gmail.com'),
             Apartment.objects.get(owner__email='apartment_owner1@gmail.com')),
            (Seeker.objects.get(base_user__email='seeker2@gmail.com'),
             Apartment.objects.get(owner__email='apartment_owner2@gmail.com')),
        ]
        with transaction.atomic():
            for seeker, apartment in connection_test_data:
                Connection(seeker=seeker, apartment=apartment).save()

    operations = [
        migrations.RunPython(generate_connection_data)
        ]
