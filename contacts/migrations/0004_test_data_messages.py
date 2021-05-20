from django.db import migrations, transaction
from contacts.models import Connection, Message


class Migration(migrations.Migration):
    dependencies = [
        ('contacts', '0003_test_data_contacts'),
    ]

    def generate_message_data(apps, schema_editor):
        message_test_data = [
            ('Hey there!'),
            ('Howdy!'),
        ]
        with transaction.atomic():
            connection = Connection.objects.last()
            Message(connection=connection, author=connection.seeker.base_user, text=message_test_data[0]).save()
            Message(connection=connection, author=connection.apartment.owner, text=message_test_data[1]).save()

    operations = [
        migrations.RunPython(generate_message_data)
        ]
