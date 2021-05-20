from django.db import migrations, transaction
from users.models import Hobby


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_test_data_cities'),
    ]

    def generate_hobby_data(apps, schema_editor):
        hobby_test_data = [
            ('Reading'),
            ('Watching TV'),
            ('Family Time'),
            ('Movies'),
            ('Fishing'),
            ('Computer'),
            ('Gardening'),
            ('Painting'),
            ('Walking'),
            ('Exercise'),
            ('Listening to Music'),
            ('Entertaining'),
            ('Hunting'),
            ('Team Sports'),
            ('Shopping'),
            ('Traveling'),
            ('Sleeping'),
            ('Socializing'),
            ('Sewing'),
            ('Golf'),
            ('Church Activities'),
            ('Relaxing'),
            ('Playing Music'),
            ('Housework'),
            ('Crafts'),
            ('Watching Sports'),
            ('Bicycling'),
            ('Playing Cards'),
            ('Hiking'),
            ('Cooking'),
            ('Eating Out'),
            ('Dating Online'),
            ('Swimming'),
            ('Camping'),
            ('Skiing'),
            ('Working on Cars'),
            ('Writing'),
            ('Boating'),
            ('Motorcycling'),
            ('Animal Care'),
            ('Bowling'),
            ('Snooker'),
            ('Running'),
            ('Diving'),
            ('Watching Netflix'),
            ('Gaming'),
            ('CTFs'),
            ('Basketball'),
            ('Sports fan'),
            ('Solving problems'),
        ]
        with transaction.atomic():
            for hob in hobby_test_data:
                Hobby(name=hob).save()

    operations = [
        migrations.RunPython(generate_hobby_data),
    ]
