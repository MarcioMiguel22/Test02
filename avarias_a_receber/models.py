from django.db import models

class Avaria(models.Model):
    localizacao = models.CharField(max_length=255)
    instalacao = models.CharField(max_length=255)
    descricao_da_avaria = models.TextField(blank=True, null=True)
    data_da_avaria = models.CharField(max_length=255)
    fim_da_avaria = models.CharField(max_length=255, blank=True, null=True)
    estado_do_elevador = models.CharField(max_length=255)
    pago = models.CharField(max_length=3, choices=[('Sim', 'Sim'), ('Não', 'Não')], default='Não')
    notas = models.TextField(blank=True, null=True)
    inicio_deslocacao1 = models.CharField(max_length=255, blank=True, null=True)
    fim_deslocacao1 = models.CharField(max_length=255, blank=True, null=True)
    inicio_deslocacao2 = models.CharField(max_length=255, blank=True, null=True)
    fim_deslocacao2 = models.CharField(max_length=255, blank=True, null=True)
    codigo_material = models.CharField(max_length=255, blank=True, null=True)
    descricao_material = models.CharField(max_length=255, blank=True, null=True)
    current_user = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.localizacao} - {self.instalacao} - {self.data_da_avaria}"

class Material(models.Model):
    codigo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

class RatesConfiguration(models.Model):
    standard_rate = models.DecimalField(max_digits=6, decimal_places=2, default=12.00)
    stop_rate = models.DecimalField(max_digits=6, decimal_places=2, default=11.00)
    after_11pm_surcharge = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)
    current_user = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        unique_together = ('current_user',)
    
    def __str__(self):
        return f"Rates Configuration for {self.current_user or 'Default'}"
