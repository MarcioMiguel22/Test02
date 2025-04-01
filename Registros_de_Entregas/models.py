from django.db import models  # Importação do módulo models do Django para definição de modelos
import uuid  # Importação do módulo uuid para geração de identificadores únicos
from django.utils import timezone  # Importação do módulo timezone para manipulação de datas e horas
import json  # Importação do módulo json para manipulação de dados JSON
from django.contrib.auth.models import User  # Importação do modelo User do Django para relacionamentos

class RegistroEntrega(models.Model):
    """
    Modelo para armazenar registros de entregas de trabalhos, obras, requisições, etc.
    Este modelo representa a estrutura de dados para documentar a entrega e acompanhamento
    de diferentes tipos de trabalhos e serviços realizados.
    """
    
    # Lista de opções para o tipo de documento
    # Cada opção consiste em um par (valor_armazenado, descrição_apresentada)
    TIPO_DOCUMENTO_CHOICES = [
        ('trabalho_directo_faturar', '1. Trabalho Directo a Facturar'),  # Trabalhos com faturamento direto
        ('trabalho_directo_contrato', '2. Trabalho Directo (Contracto Completo)'),  # Trabalhos cobertos por contratos
        ('obra', '3. Obra'),  # Obras completas
        ('requisicao_material', '4. Requisição de Material'),  # Pedidos de materiais
        ('retirada_lixo', '5. Pedido de Retirada de Lixo das Instalações'),  # Solicitações de remoção de resíduos
        ('marcacao_ferias', '6. Marcação de Férias'),  # Agendamento de férias
        ('outros', '7. Outros'),  # Outros tipos de documentos
    ]
    
    # Campos do modelo
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Identificador único universal como chave primária
    obra_id = models.CharField(max_length=100, verbose_name="ID da Obra")  # Código identificador da obra
    data_entrega = models.DateField(verbose_name="Data de Entrega")  # Data em que o serviço/documento foi entregue
    data_entrega_doc = models.DateField(null=True, blank=True, verbose_name="Data de Entrega à Chefia")  # Data de entrega à supervisão
    data_trabalho_finalizado = models.DateField(null=True, blank=True, verbose_name="Data de Finalização")  # Data de conclusão do trabalho
    numero_instalacao = models.CharField(max_length=100, verbose_name="Número de Instalação")  # Identificador da instalação
    numero_obra = models.CharField(max_length=100, verbose_name="Número da Obra")  # Número de referência da obra
    assinatura = models.TextField(blank=True, null=True, verbose_name="Assinatura (Base64)")  # Assinatura digitalizada em formato Base64
    imagem = models.TextField(blank=True, null=True, verbose_name="Imagem (Base64)")  # Imagem principal em formato Base64
    imagens = models.TextField(null=True, blank=True, verbose_name="Imagens Adicionais")  # Armazena múltiplas imagens em formato JSON
    notas = models.TextField(blank=True, null=True, verbose_name="Observações")  # Campo para observações e comentários adicionais
    
    # Campos de auditoria para controle de datas
    data_criacao = models.DateTimeField(default=timezone.now, verbose_name="Data de Criação")  # Data de criação do registro
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")  # Data/hora automática no momento da criação
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")  # Data/hora atualizada automaticamente quando modificado
    
    # Relacionamento com o usuário que criou o registro
    criado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,  # Quando o usuário é removido, o campo é definido como NULL
        null=True, 
        blank=True, 
        related_name='registros_criados',  # Nome da relação inversa para acesso a partir do usuário
        verbose_name="Criado por"
    )
    
    # Tipo de documento selecionado a partir das opções definidas
    tipo_documento = models.CharField(
        max_length=50, 
        choices=TIPO_DOCUMENTO_CHOICES,  # Lista de opções disponíveis
        default='trabalho_directo_faturar',  # Valor padrão se nenhum for especificado
        verbose_name="Tipo de Documento",
        null=True, 
        blank=True
    )

    def get_imagens(self):
        """
        Método para recuperar a lista de imagens a partir da string JSON.
        Converte a string JSON armazenada no campo imagens em uma lista Python.
        
        Returns:
            list: Lista de imagens ou lista vazia se não houver imagens ou ocorrer erro.
        """
        if self.imagens:
            try:
                return json.loads(self.imagens)  # Converte string JSON para lista Python
            except:
                return []  # Retorna lista vazia em caso de erro na conversão
        return []  # Retorna lista vazia se não houver imagens
    
    def set_imagens(self, value):
        """
        Método para definir imagens como uma string JSON.
        Converte uma lista Python para uma string JSON para armazenamento no banco de dados.
        
        Args:
            value: Lista de imagens a ser convertida para JSON, ou None para limpar o campo.
        """
        if value is not None:
            self.imagens = json.dumps(value)  # Converte lista para string JSON
        else:
            self.imagens = None  # Limpa o campo se o valor for None

    class Meta:
        """
        Classe Meta para configuração de metadados do modelo.
        Define configurações como nome no singular, plural e ordenação padrão.
        """
        verbose_name = "Registro de Entrega"  # Nome no singular para o admin
        verbose_name_plural = "Registros de Entregas"  # Nome no plural para o admin
        ordering = ['-data_entrega']  # Ordena do mais recente para o mais antigo

    def __str__(self):
        """
        Método para representação em string do objeto.
        Define como o objeto será exibido quando convertido para string.
        
        Returns:
            str: String representando o registro de entrega.
        """
        return f"Obra #{self.numero_obra} - Instalação #{self.numero_instalacao}"
