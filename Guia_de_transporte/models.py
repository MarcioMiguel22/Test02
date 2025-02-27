"""
Documento de Modelos para Guia de Transporte.
Define a estrutura de dados para as Guias de Transporte,
incluindo campos como item, descrição, unidade, quantidade, peso e volume.
"""
from django.db import models

class GuiaDeTransporte(models.Model):
    item = models.CharField(max_length=100)
    descricao = models.TextField()
    unidade = models.CharField(max_length=50)
    quantidade = models.IntegerField(default=0)
    peso = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Guia de Transporte'
        verbose_name_plural = 'Guias de Transporte'

    def __str__(self):
        return f"{self.item} - {self.descricao[:50]}"
