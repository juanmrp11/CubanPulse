# Generated by Django 5.1.4 on 2025-01-07 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0040_delete_paquete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('nombre', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=20)),
                ('precio', models.FloatField()),
                ('duracion_dias', models.IntegerField()),
                ('duracion_noches', models.IntegerField()),
                ('descripcion', models.TextField(max_length=5000)),
                ('imagen', models.ImageField(upload_to='media/')),
                ('hospedaje', models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.alojamiento')),
                ('servicios', models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.servicio')),
            ],
        ),
    ]
