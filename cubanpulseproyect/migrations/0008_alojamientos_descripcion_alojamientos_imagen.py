# Generated by Django 5.1.4 on 2024-12-26 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0007_paquete_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='alojamientos',
            name='descripcion',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='alojamientos',
            name='imagen',
            field=models.ImageField(null=True, upload_to='media/'),
        ),
    ]
