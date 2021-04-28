from django.db import migrations, transaction
from seekers.models import Seeker
from apartments.models import Apartment
from contacts.models import Connection


class Migration(migrations.Migration):
    dependencies = [
        ('contacts', '0002_auto_20210428_0914'),
        ('users', '0002_test_data_users'),
    ]

    def generate_connection_data(apps, schema_editor):
        connection_test_data = [
            ('user3@hmail.com', 'user2@hmail.com'),
            ('user3@hmail.com', 'user1@hmail.com'),
        ]
        with transaction.atomic():
            for seeker_email, apartment_email in connection_test_data:
                sample_seeker = Seeker.objects.get(base_user__email=seeker_email)
                sample_apartment = Apartment.objects.get(owner__email=apartment_email)
                Connection(apartment=sample_apartment, seeker=sample_seeker).save()

    operations = [
        migrations.RunPython(generate_connection_data)
        ]
