from django.db import migrations
from contacts.models import Connection


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_test_data_contacts'),
    ]

    def clean_connection_test_data(apps, schema_editor):
        Connection.objects.all().delete()

    operations = [
        migrations.RunPython(clean_connection_test_data),
    ]
