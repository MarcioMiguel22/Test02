"""
Arquivo: models.py
Autor: (Seu nome ou equipe)
Descrição:
    Este arquivo define o modelo de dados para 'CodigoEntrada'.
    - localizacao: nome/descrição do local (pode se repetir).
    - instalacao: identificador único da instalação (unique=True).
    - codigos_da_porta: possíveis códigos de acesso (texto, separados por vírgula).
    - codigo_caves: campo adicional para código 'caves'.

Notas:
    - 'unique=True' em 'instalacao' impede registros duplicados de instalação.
    - Se houver regras de negócio específicas (ex.: validações adicionais), 
      considere sobrescrever métodos como 'clean()' ou usar signals.
"""

# O módulo django.db.models contém as classes base para criar modelos (tabelas) no Django.
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
        unique=True,  # Garante que não haja duas instalações com mesmo valor.
        help_text="Nome único ou identificador da instalação (ex: Sala 101)."
    )

    codigos_da_porta = models.TextField(
        help_text="Códigos de acesso à porta, separados por vírgula."
    )

    codigo_caves = models.CharField(
        max_length=255,
        help_text="Código adicional (por exemplo, 'caves')."
    )

    def __str__(self) -> str:
        """
        Retorna uma representação amigável, útil para o Django admin e outros locais.
        """
        return f"{self.localizacao} - {self.instalacao}"

    class Meta:
        """
        Configurações adicionais do modelo.
        """
        ordering = ['localizacao']  # Ordena a listagem pelo campo 'localizacao'
        # Removemos unique_together para permitir várias localizações repetidas 
        # e manter apenas a restrição de unicidade em 'instalacao'.
