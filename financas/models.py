from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    cor = models.CharField(max_length=7, default='#FFFFFF')
    orcamento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    icone = models.CharField(max_length=50, default='default_icon')  # Ajustado o default para uma string
    padrao = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Subcategoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    cor = models.CharField(max_length=7, default='#FFFFFF')
    orcamento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    icone = models.CharField(max_length=50, default='default_icon')  # Ajustado o default para uma string
    padrao = models.BooleanField(default=False)
    
    # Relacionamento com uma categoria pai, se necessário
    categoria_pai = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategorias'
    )

    class Meta:
        verbose_name = "Subcategoria"
        verbose_name_plural = "Subcategorias"

    def __str__(self):
        return self.nome


class Transacao(models.Model):
    TIPOS = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]
    
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='transacoes'
    )
    nome = models.CharField(max_length=100, null=True)
    descricao = models.TextField(null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo}/{self.categoria}: {self.valor}'


#add cartao e contas aqui

class Limites(models.Model):
    RECORRENCIA_CHOICES = [
        ('mensal', 'Mensal'),
        ('diario', 'Diário'),
        ('semanal', 'Semanal'),
        ('anual', 'Anual'),
    ]
    
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='limits'
    )
    titulo = models.CharField(max_length=200, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    recorrencia = models.CharField(max_length=10, choices=RECORRENCIA_CHOICES)
    data_inicio = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.titulo} - {self.categoria}'


class Meta(models.Model):
    titulo = models.CharField(max_length=200)
    valor_meta = models.DecimalField(max_digits=10, decimal_places=2)
    valor_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='metas'
    )
    imagem = models.ImageField(upload_to='metas/', null=True, blank=True)

    def __str__(self):
        return self.titulo

    @property
    def porcentagem_concluida(self):
        if self.valor_meta:
            return min(100, (self.valor_atual / self.valor_meta) * 100)
        return 0



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


class Cartao(models.Model):
    BANDEIRAS = (
        ('MASTER', 'Mastercard'),
        ('INTER', 'Inter'),
    )
    
    STATUS = (
        ('ABERTA', 'Aberta'),
        ('FECHADA', 'Fechada'),
    )
    
    tipo_cartao = models.CharField(max_length=10, choices=BANDEIRAS)
    nome_cartao = models.CharField(max_length=100)
    data_fechamento = models.DateField()
    data_vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS, default='ABERTA')
    
    class Meta:
        verbose_name = 'Cartão'
        verbose_name_plural = 'Cartões'
        
    def __str__(self):
        return self.nome_cartao
        
    def valor_fatura(self):
        transacoes = self.transacao_set.all()
        return sum(t.valor for t in transacoes)