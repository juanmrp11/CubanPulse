# Generated by Django 5.1.4 on 2024-12-27 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0021_delete_paquete_delete_servicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('nombre', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('descripcion', models.TextField(max_length=1000)),
                ('precio', models.FloatField()),
                ('pedido', models.BooleanField(default=False)),
                ('tipo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('nombre', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=20)),
                ('precio', models.FloatField()),
                ('descripcion', models.TextField(max_length=5000)),
                ('alojamiento', models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.alojamiento')),
                ('imagen', models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.imagen')),
                ('servicios', models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.servicio')),
            ],
        ),
    ]
