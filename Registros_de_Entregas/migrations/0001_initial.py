# Generated by Django 5.1.6 on 2025-03-09 11:29

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroEntrega',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('obra_id', models.CharField(max_length=100, verbose_name='ID da Obra')),
                ('data_entrega', models.DateField(verbose_name='Data de Entrega')),
                ('numero_instalacao', models.CharField(max_length=100, verbose_name='Número de Instalação')),
                ('numero_obra', models.CharField(max_length=100, verbose_name='Número da Obra')),
                ('assinatura', models.TextField(blank=True, null=True, verbose_name='Assinatura (Base64)')),
                ('imagem', models.TextField(blank=True, null=True, verbose_name='Imagem (Base64)')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Registro de Entrega',
                'verbose_name_plural': 'Registros de Entregas',
                'ordering': ['-data_entrega'],
            },
        ),
    ]
