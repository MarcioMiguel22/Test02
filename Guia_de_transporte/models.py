from django.db import models

# Create your models here.

from django.db import models

class TransportItem(models.Model):
    item = models.CharField(max_length=255)
    descricao = models.TextField()
    unidade = models.CharField(max_length=50)
    quantidade = models.IntegerField()
    peso = models.FloatField()
    volume = models.FloatField()

    def __str__(self):
        return self.item
