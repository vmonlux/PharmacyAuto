# Generated by Django 5.0.1 on 2024-11-01 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0003_refrigerator_broken'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefrigeratorModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ModelName', models.CharField(blank=True, max_length=50, null=True)),
                ('Screen', models.BooleanField(default=False)),
                ('Window', models.BooleanField(default=False)),
                ('InteriorVolume', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('Height', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('Width', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('Depth', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
