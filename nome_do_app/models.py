# O módulo django.db.models é onde estão definidas as classes base para criar
# modelos (tabelas) no Django. Aqui importamos esse módulo para poder definir
# nossas tabelas.
from django.db import models

# A classe CodigoEntrada representa uma tabela no banco de dados, onde cada
# instância dessa classe será um registro na tabela.
class CodigoEntrada(models.Model):
    # localizacao: armazenará informações sobre a localização (ex: nome de um prédio).
    # É um CharField, ou seja, um campo do tipo string com tamanho máximo de 255 caracteres.
    localizacao = models.CharField(max_length=255)

    # instalacao: armazenará informações sobre a instalação em que o código
    # está relacionado (ex: sala, andar, etc.). Também é um CharField com
    # tamanho máximo de 255 caracteres.
    instalacao = models.CharField(max_length=255)

    # codigos_da_porta: campo para armazenar códigos da porta. Usamos TextField
    # pois pode conter múltiplos códigos separados por vírgula, por exemplo.
    # É um texto mais longo do que um CharField simples.
    codigos_da_porta = models.TextField()  # Armazena como string separada por vírgulas

    # codigo_caves: armazena algum tipo de código relacionado a "caves"
    # (termos específicos do projeto). É um CharField com limite de 255 caracteres.
    codigo_caves = models.CharField(max_length=255)

    # O método __str__ define como o objeto será representado como string
    # (útil para exibição no Django admin, por exemplo).
    def __str__(self):
        return f"{self.localizacao} - {self.instalacao}"

    # A classe Meta permite definir configurações adicionais do modelo.
    # Aqui, estamos definindo a ordenação padrão pela coluna 'localizacao'.
    class Meta:
        ordering = ['localizacao']
