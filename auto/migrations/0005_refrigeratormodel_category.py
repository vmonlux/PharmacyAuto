# Generated by Django 5.0.1 on 2024-11-20 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0004_refrigeratormodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='refrigeratormodel',
            name='Category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
