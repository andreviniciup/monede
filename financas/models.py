from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
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
    cor = models.CharField(max_length=7, default='#FFFFFF')
    orcamento = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Definindo um valor padrão
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
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


class DespesaPlanejada(models.Model):
    nome = models.CharField(max_length=100)
    cor = models.CharField(max_length=20)  # Exemplo: 'yellow', 'purple', etc.
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_gasto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

    @property
    def valor_faltante(self):
        return self.valor_total - self.valor_gasto

    @property
    def percentual_gasto(self):
        return (self.valor_gasto / self.valor_total) * 100
    
class Pagamento(models.Model):
    FREQUENCIA_CHOICES = [
        ('unica', 'Única'),
        ('mensal', 'Mensal'),
        ('anual', 'Anual'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('atrasado', 'Atrasado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    frequencia = models.CharField(max_length=10, choices=FREQUENCIA_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['data_vencimento']

    def __str__(self):
        return f"{self.titulo} - R${self.valor} ({self.get_status_display()})"

    def esta_atrasado(self):
        return self.data_vencimento < timezone.now().date() and self.status == 'pendente'


class Meta(models.Model):
    titulo = models.CharField(max_length=200)
    valor_meta = models.DecimalField(max_digits=10, decimal_places=2)
    valor_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    imagem = models.ImageField(upload_to='metas/', null=True, blank=True)
    
    def __str__(self):
        return self.titulo

    @property
    def porcentagem_concluida(self):
        if self.valor_meta:
            return min(100, (self.valor_atual / self.valor_meta) * 100)
        return 0
