# Generated by Django 5.0.1 on 2024-01-23 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Omnicell',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Omni_Id', models.CharField(blank=True, max_length=50, null=True)),
                ('Omni_Description', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Refrigerator',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Facilities_Id', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
