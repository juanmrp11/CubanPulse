# Generated by Django 5.1.4 on 2024-12-26 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0009_alojamientos_reservado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamientos',
            name='reservado',
            field=models.BooleanField(default=False),
        ),
    ]
