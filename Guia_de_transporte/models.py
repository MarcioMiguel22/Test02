"""
Documento de Modelos para Guia de Transporte.
Define a estrutura de dados para as Guias de Transporte,
incluindo campos como item, descrição, unidade, quantidade, notas e volume.
"""
from django.db import models

class GuiaDeTransporte(models.Model):
    item = models.CharField(max_length=100)
    descricao = models.TextField()
    unidade = models.CharField(max_length=50, default='UN')  # Campo adicionado
    quantidade = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Campo adicionado
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Campo adicionado
    notas = models.TextField(blank=True, null=True)
    em_falta = models.CharField(max_length=255, null=True, blank=True)
    total = models.CharField(max_length=50, default='0')
    imagem = models.TextField(blank=True, null=True)  # Campo adicionado do TransportItem
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'guia_de_transporte_guiadetransporte'
        verbose_name = 'Guia de Transporte'
        verbose_name_plural = 'Guias de Transporte'

    def __str__(self):
        return f"{self.item} - {self.descricao[:50]}"

class TransportItem(models.Model):
    item = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    unidade = models.CharField(max_length=50, default='UN')
    quantidade = models.IntegerField(default=0)
    em_falta = models.CharField(max_length=50, default='0')
    total = models.CharField(max_length=50, default='0')
    notas = models.TextField(blank=True, null=True)
    imagem = models.TextField(blank=True, null=True)  # Base64 encoded image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item} - {self.descricao}"
