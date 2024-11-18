from django import forms
from .models import Transacao, Pagamento, Categoria, Subcategoria, Cartao, TransacaoCartao, Banco, Conta

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['valor', 'tipo', 'categoria', 'descricao']
        

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['titulo', 'valor', 'data_vencimento', 'frequencia']
        widgets = {
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}),
            'valor': forms.NumberInput(attrs={'step': '0.01'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'cor', 'icone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'campo-formulario', 'placeholder': 'Ex: cofrinho'}),
            'cor': forms.HiddenInput(),
            'icone': forms.HiddenInput(),
        }

class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nome', 'cor', 'icone', 'categoria_pai']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'campo-formulario', 'placeholder': 'Ex: despesas extras'}),
            'cor': forms.HiddenInput(),
            'icone': forms.HiddenInput(),
            'categoria_pai': forms.Select(attrs={'class': 'campo-formulario'}),
        }

class CartaoForm(forms.ModelForm):
    class Meta:
        model = Cartao
        fields = ['nome_cartao', 'tipo_cartao', 'data_fechamento', 'data_vencimento']
        widgets = {
            'data_fechamento': forms.DateInput(attrs={'type': 'date'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}),
        }


class TransacaoCartaoForm(forms.ModelForm):
    class Meta:
        model = TransacaoCartao
        fields = ['valor', 'descricao', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ['nome', 'icone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'icone': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['banco', 'titulo', 'saldo']
        widgets = {
            'banco': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }