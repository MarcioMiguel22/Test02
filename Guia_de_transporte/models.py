"""
Documento de Modelos para Guia de Transporte.
Define a estrutura de dados para as Guias de Transporte,
incluindo campos como item, descrição, unidade, quantidade, notas e volume.
"""
from django.db import models

class GuiaDeTransporte(models.Model):
    item = models.CharField(max_length=100)
    descricao = models.TextField()
    em_falta = models.IntegerField()  # Alterado para IntegerField para armazenar números
    quantidade = models.IntegerField()
    notas = models.TextField(blank=True, null=True)  # Alterado para TextField para permitir texto longo
    total = models.IntegerField(default=0)  # Adicionar valor padrão
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'guia_de_transporte_guiadetransporte'
        verbose_name = 'Guia de Transporte'
        verbose_name_plural = 'Guias de Transporte'

    def __str__(self):
        return f"{self.item} - {self.descricao[:50]}"
