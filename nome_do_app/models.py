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
        max_length=255,  # Removido unique=True
        help_text="Nome ou identificador da instalação (ex: 'Sala 101')."
    )
    codigos_da_porta = models.TextField(
        help_text="Códigos de acesso à porta, separados por vírgula."
    )
    codigo_caves = models.CharField(
        max_length=255,
        help_text="Código adicional (por exemplo, 'caves')."
    )

    def __str__(self) -> str:
        return f"{self.localizacao} - {self.instalacao}"

    class Meta:
        ordering = ['localizacao']  # Ordena listagens pelo campo 'localizacao'
