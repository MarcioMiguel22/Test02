from django.db import models

# Create your models here.
from django.db import models

class CodigoEntrada(models.Model):
    localizacao = models.CharField(max_length=255)
    instalacao = models.CharField(max_length=255)
    codigos_da_porta = models.TextField()  # Store as comma-separated string
    codigo_caves = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.localizacao} - {self.instalacao}"

    class Meta:
        ordering = ['localizacao']
