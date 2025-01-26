from django.db import models

class Resposta(models.Model):
    numero_instalacao = models.CharField(max_length=100)
    pergunta_id = models.IntegerField()
    resposta = models.TextField()
    comentario = models.TextField(blank=True, null=True)
    tecnico = models.CharField(max_length=100, blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)  # Adiciona rastreamento de modificações

    def __str__(self):
        return f"Instalação {self.numero_instalacao} - Pergunta {self.pergunta_id}"
