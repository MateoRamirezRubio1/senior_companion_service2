# Generated by Django 4.2.4 on 2023-11-15 01:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeAvailability',
            fields=[
                ('idTimeAvailability', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(null=True)),
                ('startTime', models.TimeField(null=True)),
                ('endTime', models.TimeField(null=True)),
                ('idCompanion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companion.companion')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('idSkill', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('idCompanion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companion.companion')),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('idReference', models.AutoField(primary_key=True, serialize=False)),
                ('names', models.CharField(max_length=80, null=True)),
                ('lastNames', models.CharField(max_length=80, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('address', models.CharField(max_length=60, null=True)),
                ('email', models.CharField(max_length=60, null=True, unique=True)),
                ('idCompanion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companion.companion')),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('idCertification', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=45)),
                ('certificate', models.FileField(upload_to='certificates/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('idCompanion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companion.companion')),
            ],
        ),
    ]
