# Generated by Django 5.1.6 on 2025-03-02 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guia_de_transporte', '0001_initial_squashed_0006_add_em_falta_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guiadetransporte',
            old_name='unidade',
            new_name='em_falta',
        ),
        migrations.RemoveField(
            model_name='guiadetransporte',
            name='volume',
        ),
        migrations.AlterField(
            model_name='guiadetransporte',
            name='total',
            field=models.CharField(default='0', max_length=50),
        ),
    ]
