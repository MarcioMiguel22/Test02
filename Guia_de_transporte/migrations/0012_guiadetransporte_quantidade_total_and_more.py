# Generated by Django 4.2.20 on 2025-03-17 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guia_de_transporte', '0011_guiadetransporte_current_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guiadetransporte',
            name='quantidade_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transportitem',
            name='quantidade_total',
            field=models.IntegerField(default=0),
        ),
    ]
