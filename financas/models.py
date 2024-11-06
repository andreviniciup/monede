from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db import models

class Transacao(models.Model):
    TIPOS = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]
    CATEGORIAS = [
        ('CONTA_FIXA', 'Conta Fixa'),
        ('COMPRA', 'Compra'),
        ('INVESTIMENTO', 'Investimento'),
        ('LAZER', 'Lazer'),
    ]
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    categoria = models.CharField(max_length=15, choices=CATEGORIAS)
    nome = models.CharField(max_length=100, null=True)
    descricao = models.TextField(null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)  # Define data e hora automaticamente

    def __str__(self):
        return f'{self.tipo}/{self.categoria}: {self.valor}'



class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    # Outros campos personalizados
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )
