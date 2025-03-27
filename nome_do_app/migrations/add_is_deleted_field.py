from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('nome_do_app', '0001_initial'),  # Adjust this to your latest migration
    ]

    operations = [
        migrations.AddField(
            model_name='codigoentrada',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='Flag para exclusão lógica'),
        ),
    ]
