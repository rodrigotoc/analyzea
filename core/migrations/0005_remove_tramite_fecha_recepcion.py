# Generated by Django 3.2.18 on 2023-04-05 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_estadotramite_tramite_padre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tramite',
            name='fecha_recepcion',
        ),
    ]
