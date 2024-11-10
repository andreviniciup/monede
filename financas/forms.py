from django import forms
from .models import Transacao, Pagamento

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