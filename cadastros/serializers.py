from dataclasses import fields
from rest_framework import serializers

from .models import Fornecedor

class FornecedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fornecedor
        fields = ['id', 'nome', 'ativo']