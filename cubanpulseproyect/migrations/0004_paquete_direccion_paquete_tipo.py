# Generated by Django 5.1.4 on 2024-12-25 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0003_alter_paquete_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='direccion',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='paquete',
            name='tipo',
            field=models.CharField(max_length=50, null=True),
        ),
    ]