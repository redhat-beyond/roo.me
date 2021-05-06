from django.db import migrations, transaction
from apartments.models import City


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_clean_test_data'),
    ]

    def generate_city_data(apps, schema_editor):
        city_test_data = [
            ('Jerusalem'),
            ('Tel Aviv'),
            ('Haifa'),
            ('Ashdod'),
            ('Rishon LeZiyyon'),
            ('Petah Tiqwa'),
            ('Beersheba'),
            ('Netanya'),
            ('Holon'),
            ('Bnei Brak'),
            ('Rehovot'),
            ('Bat Yam'),
            ('Ramat Gan'),
            ('Ashkelon'),
            ('Jaffa'),
            ('Modiin'),
            ('Herzliya'),
            ('Kfar Saba'),
            ('Raanana'),
            ('Hadera'),
            ('Bet Shemesh'),
            ('Lod'),
            ('Nazareth'),
            ('Atlit'),
            ('Ramla'),
            ('Nahariyya'),
            ('Qiryat Ata'),
            ('Givatayim'),
            ('Qiryat Gat'),
            ('Acre'),
            ('Eilat'),
            ('Afula'),
            ('Karmiel'),
            ('Hod HaSharon'),
            ('Umm el Fahm'),
            ('Tiberias'),
            ('Qiryat Mozqin'),
            ('Qiryat Yam'),
            ('Rosh HaAyin'),
            ('Ness Ziona'),
            ('Qiryat Bialik'),
            ('Ramat HaSharon'),
            ('Dimona'),
            ('Taiyiba'),
            ('Yavne'),
            ('Or Yehuda'),
            ('Qiryat Shemona'),
            ('Kefar Yona'),
            ('Shoham'),
            ('Pardesiya'),
        ]
        with transaction.atomic():
            for name in city_test_data:
                City(cityName=name).save()

    operations = [
        migrations.RunPython(generate_city_data),
    ]
