from django.db import models
import uuid
from django.utils import timezone
import json
from django.contrib.auth.models import User

class RegistroEntrega(models.Model):
    # Document type choices
    TIPO_DOCUMENTO_CHOICES = [
        ('trabalho_directo_faturar', '1. Trabalho Directo a Facturar'),
        ('trabalho_directo_contrato', '2. Trabalho Directo (Contracto Completo)'),
        ('obra', '3. Obra'),
        ('requisicao_material', '4. Requisição de Material'),
        ('retirada_lixo', '5. Pedido de Retirada de Lixo das Instalações'),
        ('marcacao_ferias', '6. Marcação de Férias'),
        ('outros', '7. Outros'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    obra_id = models.CharField(max_length=100, verbose_name="ID da Obra")
    data_entrega = models.DateField(verbose_name="Data de Entrega")
    data_entrega_doc = models.DateField(null=True, blank=True, verbose_name="Data de Entrega à Chefia")
    data_trabalho_finalizado = models.DateField(null=True, blank=True, verbose_name="Data de Finalização")
    numero_instalacao = models.CharField(max_length=100, verbose_name="Número de Instalação")
    numero_obra = models.CharField(max_length=100, verbose_name="Número da Obra")
    assinatura = models.TextField(blank=True, null=True, verbose_name="Assinatura (Base64)")
    imagem = models.TextField(blank=True, null=True, verbose_name="Imagem (Base64)")
    imagens = models.TextField(null=True, blank=True, verbose_name="Imagens Adicionais")
    notas = models.TextField(blank=True, null=True, verbose_name="Observações")
    data_criacao = models.DateTimeField(default=timezone.now, verbose_name="Data de Criação")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='registros_criados', verbose_name="Criado por")
    tipo_documento = models.CharField(
        max_length=50, 
        choices=TIPO_DOCUMENTO_CHOICES,
        default='trabalho_directo_faturar',
        verbose_name="Tipo de Documento",
        null=True, 
        blank=True
    )

    def get_imagens(self):
        """Get images as a list from JSON string"""
        if self.imagens:
            try:
                return json.loads(self.imagens)
            except:
                return []
        return []
    
    def set_imagens(self, value):
        """Set images as JSON string"""
        if value is not None:
            self.imagens = json.dumps(value)
        else:
            self.imagens = None

    class Meta:
        verbose_name = "Registro de Entrega"
        verbose_name_plural = "Registros de Entregas"
        ordering = ['-data_entrega']

    def __str__(self):
        return f"Obra #{self.numero_obra} - Instalação #{self.numero_instalacao}"
