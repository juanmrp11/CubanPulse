# Generated by Django 5.1.4 on 2025-01-10 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0051_remove_alojamiento_cant_habitaciones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paquete',
            name='precio',
        ),
    ]
