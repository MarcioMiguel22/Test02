from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('Guia_de_transporte', '0001_initial_squashed_0006_add_em_falta_total'),
    ]

    operations = [
        # Check if the column exists before trying to add it
        migrations.RunSQL(
            sql="""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_name = 'guia_de_transporte_guiadetransporte' 
                    AND column_name = 'em_falta'
                ) THEN
                    ALTER TABLE guia_de_transporte_guiadetransporte 
                    ADD COLUMN em_falta VARCHAR(255) NULL;
                END IF;
            END $$;
            """,
            reverse_sql="""
            ALTER TABLE guia_de_transporte_guiadetransporte 
            DROP COLUMN IF EXISTS em_falta;
            """
        ),
    ]
