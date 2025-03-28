from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.postgres.fields import ArrayField

class DespesaCarro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='despesas_carro')
    
    # Campos principais
    tipo_combustivel = models.CharField(max_length=50)
    valor_despesa = models.DecimalField(max_digits=10, decimal_places=2)
    data_despesa = models.DateField()
    quilometragem = models.PositiveIntegerField()
    
    # Campos opcionais
    observacoes = models.TextField(null=True, blank=True)
    
    # Campos para imagens
    imagem = models.TextField(null=True, blank=True)  # Para compatibilidade
    imagens = ArrayField(models.TextField(), default=list, blank=True)
    
    # Metadados
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    usuario_criacao = models.CharField(max_length=150, null=True, blank=True)
    
    class Meta:
        ordering = ['-data_despesa']
        verbose_name = 'Despesa de Carro'
        verbose_name_plural = 'Despesas de Carro'
    
    def __str__(self):
        return f"{self.tipo_combustivel} - {self.data_despesa} - {self.valor_despesa}"
