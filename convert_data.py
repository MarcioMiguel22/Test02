"""
Data conversion script to convert string values in em_falta to integers
Run this after migrations have been applied.
"""
from Guia_de_transporte.models import GuiaDeTransporte

def convert_text_to_int():
    # Create a mapping for text values to integers
    text_to_int_map = {
        'UN': 1,
        'KG': 2,
        'L': 3,
        # Add any other values that exist in your database
    }

    # Update all records with string values
    for guia in GuiaDeTransporte.objects.all():
        if isinstance(guia.em_falta, str):
            guia.em_falta = text_to_int_map.get(guia.em_falta, 0)
            guia.save()
            print(f'Updated {guia.item}: {guia.em_falta}')
        else:
            print(f'Skipping {guia.item}: already an integer ({guia.em_falta})')

if __name__ == "__main__":
    print("Starting data conversion...")
    convert_text_to_int()
    print("Data conversion completed!")
