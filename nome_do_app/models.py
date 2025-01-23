#MODELS.PY

"""
Arquivo: models.py
Descrição:
    Modelo de dados para 'CodigoEntrada'.
    - localizacao: campo textual (pode não ser único).
    - instalacao: campo textual, mas com unique=True.
    - codigos_da_porta: texto (separado por vírgula).
    - codigo_caves: campo textual adicional.
"""

from django.db import models


class CodigoEntrada(models.Model):
    """
    Representa uma entrada de código (porta/caves) para uma instalação específica.
    """
    localizacao = models.CharField(max_length=255)
    instalacao = models.CharField(max_length=255, unique=True)
    codigos_da_porta = models.TextField()
    codigo_caves = models.CharField(max_length=255)
    local_de_chaves = models.CharField(max_length=255)
    tipo_de_contrato = models.CharField(max_length=255)
    administracao = models.CharField(max_length=255)

    def __str__(self):
        return self.localizacao

    class Meta:
        ordering = ['localizacao']  # Ordena listagens pelo campo 'localizacao'
