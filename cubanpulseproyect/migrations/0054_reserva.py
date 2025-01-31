# Generated by Django 5.1.4 on 2025-01-11 08:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0053_remove_paquete_duracion_dias_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('precio_total', models.FloatField()),
                ('alojamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubanpulseproyect.alojamiento')),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubanpulseproyect.paquete')),
                ('servicios', models.ManyToManyField(related_name='reservas', to='cubanpulseproyect.servicio')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
