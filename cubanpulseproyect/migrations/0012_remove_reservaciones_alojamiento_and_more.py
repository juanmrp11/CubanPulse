# Generated by Django 5.1.4 on 2024-12-26 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0011_alojamientos_paquete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservaciones',
            name='alojamiento',
        ),
        migrations.RemoveField(
            model_name='reservaciones',
            name='viajes',
        ),
    ]
