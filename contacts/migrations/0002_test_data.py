from django.db import migrations, transaction
from users.models import Apartment, Seeker
from contacts.models import Connection


class Migration(migrations.Migration):
    dependencies = [
        ('contacts', '0001_initial'),
        ('users', '0006_test_data'),
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
