# Generated by Django 5.1.4 on 2025-01-07 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0038_remove_paquete_servicios_delete_servicio'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='paquete',
            name='servicios',
            field=models.ManyToManyField(related_name='paquete', to='cubanpulseproyect.servicio'),
        ),
    ]
