from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

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

def transacoes_view(request):
    return render(request, 'financas/transacoes.html')

def relatorios_view(request):
    return render(request, 'financas/relatorios.html')

def metas_view(request):
    return render(request, 'financas/metas.html')

def perfil_view(request):
    return render(request, 'financas/perfil.html')

