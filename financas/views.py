from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Transacao
from .forms import TransacaoForm


def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registrar.html', {'form': form})


def home_view(request):
    return render(request, 'financas/home.html')


from django.contrib import messages

def transacoes_view(request):
    transacoes = Transacao.objects.all()

    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.save()
            messages.success(request, 'Transação adicionada com sucesso.')
            return redirect('transacoes')
        else:
            messages.error(request, 'Erro ao adicionar transação. Verifique os dados e tente novamente.')
    else:
        form = TransacaoForm()

    return render(request, 'financas/transacoes.html', {'transacoes': transacoes, 'form': form})


def relatorios_view(request):
    return render(request, 'financas/relatorios.html')

def metas_view(request):
    return render(request, 'financas/metas.html')

def perfil_view(request):
    return render(request, 'financas/perfil.html')

