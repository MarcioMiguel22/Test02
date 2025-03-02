from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Guia_de_transporte', '0005_alter_guiadetransporte_notas'),
    ]

    operations = [
        # Não fazer nada, apenas marcar a migração como aplicada
        migrations.RunSQL(
            "SELECT 1;",  # SQL que não faz nada
            reverse_sql="SELECT 1;"
        ),
    ]
