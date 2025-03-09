from django.db import models

# Create your models here.
from django.db import models
import uuid

class RegistroEntrega(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    obra_id = models.CharField(max_length=100, verbose_name="ID da Obra")
    data_entrega = models.DateField(verbose_name="Data de Entrega")
    numero_instalacao = models.CharField(max_length=100, verbose_name="Número de Instalação")
    numero_obra = models.CharField(max_length=100, verbose_name="Número da Obra")
    assinatura = models.TextField(blank=True, null=True, verbose_name="Assinatura (Base64)")
    imagem = models.TextField(blank=True, null=True, verbose_name="Imagem (Base64)")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Registro de Entrega"
        verbose_name_plural = "Registros de Entregas"
        ordering = ['-data_entrega']

    def __str__(self):
        return f"Obra #{self.numero_obra} - Instalação #{self.numero_instalacao}"
