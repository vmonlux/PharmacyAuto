# Generated by Django 5.0.1 on 2024-02-14 07:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['Name'],
            },
        ),
        migrations.CreateModel(
            name='OmnicellModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Generation', models.CharField(blank=True, max_length=5, null=True)),
                ('Model', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['Generation', 'Model'],
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['Name'],
            },
        ),
        migrations.CreateModel(
            name='Omnicell',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Omni_Id', models.CharField(blank=True, max_length=50, null=True)),
                ('Omni_Description', models.CharField(blank=True, max_length=50, null=True)),
                ('Serial_Number', models.CharField(blank=True, max_length=7, null=True)),
                ('CT_Version', models.CharField(blank=True, max_length=10, null=True)),
                ('PC_Name', models.CharField(blank=True, max_length=20, null=True)),
                ('Ivanti', models.BooleanField(default=False)),
                ('Area', models.CharField(blank=True, max_length=10, null=True)),
                ('Room', models.CharField(blank=True, max_length=10, null=True)),
                ('Door_Code', models.CharField(blank=True, max_length=10, null=True)),
                ('Emergency', models.BooleanField(default=False)),
                ('Note', models.TextField(blank=True, max_length=500, null=True)),
                ('Building', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auto.building')),
                ('Model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auto.omnicellmodel')),
                ('Site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auto.site')),
            ],
            options={
                'ordering': ['Omni_Id', 'Site', 'Building', 'Area'],
            },
        ),
        migrations.CreateModel(
            name='Aux',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Serial_Number', models.CharField(blank=True, max_length=7, null=True)),
                ('Omnicell', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auto.omnicell')),
                ('Model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auto.omnicellmodel')),
            ],
            options={
                'ordering': ['Omnicell', 'Model', 'Serial_Number'],
            },
        ),
        migrations.CreateModel(
            name='Refrigerator',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Facilities_Id', models.CharField(blank=True, max_length=50, null=True)),
                ('Type', models.CharField(blank=True, max_length=50, null=True)),
                ('Omnicell', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auto.omnicell')),
            ],
            options={
                'ordering': ['Omnicell', 'Type', 'Facilities_Id'],
            },
        ),
        migrations.CreateModel(
            name='Lockbox',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Key', models.CharField(blank=True, max_length=10, null=True)),
                ('Medication', models.CharField(blank=True, max_length=50, null=True)),
                ('Description', models.CharField(blank=True, max_length=50, null=True)),
                ('Refrigerator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auto.refrigerator')),
            ],
            options={
                'ordering': ['Refrigerator'],
            },
        ),
    ]
