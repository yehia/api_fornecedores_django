from django.db import models
from django.db.models import F

class Fornecedor(models.Model):
    nome = models.CharField(max_length=200)
    ativo = models.BooleanField(default=False)

    class Meta:
        ordering = [F('nome').asc()]

    def __str__(self):
        return str(self.nome)