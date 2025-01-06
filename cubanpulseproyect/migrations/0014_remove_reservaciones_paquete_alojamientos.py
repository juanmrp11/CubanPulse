# Generated by Django 5.1.4 on 2024-12-26 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0013_delete_alojamientos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservaciones',
            name='paquete',
        ),
        migrations.CreateModel(
            name='Alojamientos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(max_length=500)),
                ('cantidad_habitaciones', models.IntegerField()),
                ('reservado', models.BooleanField(default=False)),
                ('ubicacion', models.CharField(max_length=100)),
                ('precio', models.FloatField()),
                ('imagen', models.ImageField(upload_to='media/')),
                ('nombre', models.CharField(max_length=100)),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alojamiento', to='cubanpulseproyect.paquete')),
            ],
        ),
    ]
