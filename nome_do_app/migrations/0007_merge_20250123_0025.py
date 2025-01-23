from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('nome_do_app', '0005_codigoentrada_administracao_and_more'),  # Aponta para a última migração válida
    ]

    operations = [
        migrations.AddField(
            model_name='codigoentrada',
            name='novo_campo',
            field=models.CharField(max_length=255, default='valor_padrao', help_text='Novo campo adicionado.'),
        ),
    ]
