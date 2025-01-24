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
    localizacao = models.CharField(
        max_length=255,
        help_text="Descrição do local (pode haver várias instalações no mesmo local)."
    )
    instalacao = models.CharField(
        max_length=255,
        unique=True,  # Impede duplicados neste campo
        help_text="Nome único ou identificador da instalação (ex: 'Sala 101')."
    )
    codigos_da_porta = models.TextField(
        help_text="Códigos de acesso à porta, separados por vírgula."
    )
    codigo_caves = models.CharField(
        max_length=255,
        help_text="Código adicional (por exemplo, 'caves')."
    )
    local_da_chave = models.CharField(max_length=255, blank=True)  # New field
    administracao = models.CharField(max_length=255, blank=True)   # New field
    tipo_de_contrato = models.CharField(max_length=255, blank=True)  # New field
    def __str__(self) -> str:
        return f"{self.localizacao} - {self.instalacao}"

    class Meta:
        ordering = ['localizacao']  # Ordena listagens pelo campo 'localizacao'
