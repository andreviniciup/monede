from django.db import models
from django.contrib.auth.models import User  


class Transacao(models.Model):
    CATEGORIAS = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]
    TIPOS = [
        ('CONTA_FIXA', 'Conta Fixa'),
        ('COMPRA', 'Compra'),
        ('INVESTIMENTO', 'Investimento'),
        ('LAZER', 'Lazer'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    tipo = models.CharField(max_length=15, choices=TIPOS)
    descricao = models.TextField(null=True, blank=True)
    data = models.DateField()

    def __str__(self):
        return f'{self.usuario.username} - {self.categoria}/{self.tipo}: {self.valor}'
