from django.db import models

class CodigoEntrada(models.Model):
    # Campo para armazenar a localização do acesso
    localizacao = models.CharField(max_length=255)
    
    # Campo para armazenar o nome/número da instalação
    instalacao = models.CharField(max_length=255)
    
    # Campo para armazenar os códigos da porta como texto
    # Pode armazenar múltiplos códigos separados por vírgula
    codigos_da_porta = models.TextField()
    
    # Campo para armazenar o código específico das caves
    codigo_caves = models.CharField(max_length=255)

    def __str__(self):
        # Método que define como o objeto será exibido como string
        # Exemplo: "Prédio A - Instalação 101"
        return f"{self.localizacao} - {self.instalacao}"

    class Meta:
        # Define a ordem padrão de exibição dos registros por localização
        ordering = ['localizacao']
        
        # Garante que não existam duas entradas com a mesma combinação
        # de localização e instalação no banco de dados
        unique_together = ('localizacao', 'instalacao')
