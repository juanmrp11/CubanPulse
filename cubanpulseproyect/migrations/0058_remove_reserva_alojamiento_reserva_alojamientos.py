# Generated by Django 5.1.4 on 2025-01-11 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0057_reserva'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='alojamiento',
        ),
        migrations.AddField(
            model_name='reserva',
            name='alojamientos',
            field=models.ManyToManyField(to='cubanpulseproyect.alojamiento'),
        ),
    ]
