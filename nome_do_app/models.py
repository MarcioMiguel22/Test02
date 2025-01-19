from django.db import models

class CodigoEntrada(models.Model):
    localizacao = models.CharField(max_length=255)
    instalacao = models.CharField(max_length=255)
    codigos_da_porta = models.TextField()  # Will store as comma-separated string
    codigo_caves = models.CharField(max_length=255)

    class Meta:
        ordering = ['localizacao']
        unique_together = ('localizacao', 'instalacao')

    def __str__(self):
        return f"{self.localizacao} - {self.instalacao}"

    def get_codigos_da_porta_list(self):
        return [code.strip() for code in self.codigos_da_porta.split(',') if code.strip()]

    def set_codigos_da_porta_list(self, codes_list):
        self.codigos_da_porta = ', '.join(codes_list)
