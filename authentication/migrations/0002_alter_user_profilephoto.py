# Generated by Django 4.2.4 on 2023-11-14 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profilePhoto',
            field=models.ImageField(null=True, upload_to='profile_photos/'),
        ),
    ]
