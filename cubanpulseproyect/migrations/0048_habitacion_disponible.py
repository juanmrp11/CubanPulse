# Generated by Django 5.1.4 on 2025-01-10 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubanpulseproyect', '0047_habitacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitacion',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
    ]
