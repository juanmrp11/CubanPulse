# Generated by Django 5.1.4 on 2024-12-27 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cubanpulseproyect', '0017_remove_alojamiento_imagen_remove_paquete_alojamiento_and_more'),
    ]

    operations = [
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
                ('nombre', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('precio', models.FloatField()),
                ('pedido', models.BooleanField(default=False)),
                ('tipo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Alojamiento',
            fields=[
                ('nombre', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('precio', models.FloatField()),
                ('pedido', models.BooleanField(default=False)),
                ('tipo', models.CharField(max_length=50)),
                ('cant_habitaciones', models.IntegerField()),
                ('imagen', models.ManyToManyField(related_name='alojamiento', to='cubanpulseproyect.imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('nombre', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=20)),
                ('precio', models.FloatField()),
                ('alojamiento', models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.alojamiento')),
                ('imagen', models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.imagen')),
                ('servicios', models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.servicio')),
            ],
        ),
    ]
