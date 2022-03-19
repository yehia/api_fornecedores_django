from django.urls import path

from . import views

urlpatterns = [
    path('fornecedores', views.FornecedorListAPIView.as_view(), name='fornecedores'),
    path('fornecedor/<int:id>', views.FornecedorDetailAPIView.as_view(), name='fornecedor')
]