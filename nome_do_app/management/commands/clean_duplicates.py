from django.core.management.base import BaseCommand
from nome_do_app.models import CodigoEntrada
from django.db.models import Count

class Command(BaseCommand):
    help = 'Remove duplicate CodigoEntrada entries'

    def handle(self, *args, **kwargs):
        # Find duplicates
        duplicates = (
            CodigoEntrada.objects.values('localizacao', 'instalacao')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        for dup in duplicates:
            # Get all entries for this combination
            entries = CodigoEntrada.objects.filter(
                localizacao=dup['localizacao'],
                instalacao=dup['instalacao']
            ).order_by('id')
            
            # Keep the first one, delete the rest
            first_entry = entries.first()
            entries.exclude(id=first_entry.id).delete()
            
            self.stdout.write(
                f"Cleaned duplicates for {dup['localizacao']} - {dup['instalacao']}"
            )
