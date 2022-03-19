from django.shortcuts import render

from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from .serializers import FornecedorSerializer
from .models import Fornecedor

class FornecedorListAPIView(ListCreateAPIView):
    serializer_class = FornecedorSerializer
    queryset = Fornecedor.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
class FornecedorDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = FornecedorSerializer
    queryset = Fornecedor.objects.all()
    permission_classes = (permissions.IsAuthenticated)
    lookup_field = 'id'


