# Generated by Django 3.2 on 2021-05-19 21:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seekers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0001_initial'),
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='user_messages',
                to=settings.AUTH_USER_MODEL
                ),
        ),
        migrations.AddField(
            model_name='message',
            name='connection',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='messages',
                to='contacts.connection'
                ),
        ),
        migrations.AddField(
            model_name='connection',
            name='apartment',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='apt_connection',
                to='apartments.apartment'
                ),
        ),
        migrations.AddField(
            model_name='connection',
            name='seeker',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='seeker_connection',
                to='seekers.seeker'
                ),
        ),
        migrations.AlterUniqueTogether(
            name='connection',
            unique_together={('apartment', 'seeker')},
        ),
    ]
