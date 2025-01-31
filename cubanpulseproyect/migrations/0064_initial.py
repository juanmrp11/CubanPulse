# Generated by Django 5.1.4 on 2025-01-16 07:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cubanpulseproyect', '0063_remove_alojamiento_imagen_remove_paquete_hospedaje_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Disponibilidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('disponible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='media/')),
                ('tipo', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.TextField(max_length=1000)),
                ('precio', models.FloatField()),
                ('tipo', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Alojamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('ubicacion', models.CharField(max_length=200)),
                ('descripcion', models.TextField(max_length=1500)),
                ('precio', models.FloatField(blank=True, null=True)),
                ('tipo', models.CharField(max_length=50)),
                ('reservado', models.ManyToManyField(related_name='alojamiento', to='cubanpulseproyect.disponibilidad')),
                ('imagen', models.ManyToManyField(related_name='alojamiento', to='cubanpulseproyect.imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('nombre', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=20)),
                ('descripcion', models.TextField(max_length=5000)),
                ('imagen', models.ImageField(upload_to='media/')),
                ('hospedaje', models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.alojamiento')),
                ('servicios', models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('precio_total', models.FloatField()),
                ('alojamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubanpulseproyect.alojamiento')),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubanpulseproyect.paquete')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('servicios', models.ManyToManyField(related_name='reservas', to='cubanpulseproyect.servicio')),
            ],
        ),
    ]
