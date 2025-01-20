import pandas as pd
from django.core.management.base import BaseCommand
from nome_do_app.models import CodigoEntrada  # Substitua pelo nome correto do modelo


class Command(BaseCommand):
    help = "Import data from an Excel file into the CodigoEntrada table"

    def add_arguments(self, parser):
        parser.add_argument('excel_path', type=str, help="Path to the Excel file")

    def handle(self, *args, **kwargs):
        excel_path = kwargs['excel_path']
        
        self.stdout.write(f"Starting the import process for: {excel_path}")

        try:
            # Ler dados do arquivo Excel
            self.stdout.write("Reading Excel file...")
            data = pd.read_excel(excel_path)

            self.stdout.write(f"Excel file read successfully! Total rows: {len(data)}")

            for index, row in data.iterrows():
                self.stdout.write(f"Processing row {index + 1}...")

                # Mapear os campos do Excel para os campos do banco de dados
                try:
                    CodigoEntrada.objects.update_or_create(
                        instalacao=row['Instalação'],  # Nome da coluna no Excel
                        defaults={
                            'localizacao': row['Localização'],
                            'codigos_da_porta': row['Códigos da Porta'],
                            'codigo_caves': row['Código Caves'],
                        }
                    )
                    self.stdout.write(f"Row {index + 1} imported successfully!")
                except Exception as e:
                    self.stderr.write(f"Error importing row {index + 1}: {e}")

            self.stdout.write(self.style.SUCCESS("Excel data imported successfully!"))
        except FileNotFoundError:
            self.stderr.write(f"File not found: {excel_path}")
        except Exception as e:
            self.stderr.write(f"Error importing Excel data: {e}")
