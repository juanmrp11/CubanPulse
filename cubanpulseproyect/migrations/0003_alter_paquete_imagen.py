# Generated by Django 5.1.4 on 2024-12-25 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0002_alter_paquete_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paquete',
            name='imagen',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
