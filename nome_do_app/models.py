from django.db import models

class CodigoEntrada(models.Model):
    localizacao = models.CharField(max_length=255, blank=False)
    instalacao = models.CharField(max_length=255, blank=False)
    codigos_da_porta = models.TextField(default='', blank=True)
    codigo_caves = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ['localizacao']
        unique_together = ('localizacao', 'instalacao')  # Add constraint back

    def __str__(self):
        return f"{self.localizacao} - {self.instalacao}"

    def get_codigos_da_porta_list(self):
        return [code.strip() for code in self.codigos_da_porta.split(',') if code.strip()]

    def set_codigos_da_porta_list(self, codes_list):
        self.codigos_da_porta = ', '.join(codes_list)
