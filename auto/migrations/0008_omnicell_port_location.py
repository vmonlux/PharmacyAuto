# Generated by Django 5.0.1 on 2024-11-26 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0007_portlocation_omnicell_port_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='omnicell',
            name='Port_Location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auto.portlocation'),
        ),
    ]