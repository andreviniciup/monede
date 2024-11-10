from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.http import JsonResponse
from .models import Transacao, Categoria, DespesaPlanejada, Pagamento, Meta
from .forms import TransacaoForm, PagamentoForm
import json
from datetime import datetime, timedelta

def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registrar.html', {'form': form})


def inicio_view(request):
    transacoes = Transacao.objects.order_by('-data')[:5]
    return render(request, 'financas/inicio.html', {'transacoes': transacoes})


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

def lista_metas_view(request):
    metas = Meta.objects.all()
    categorias = Categoria.objects.all()
    context = {
        'metas': metas,
        'categorias': categorias
    }
    return render(request, 'financas/metas.html', context)

def criar_meta_view(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        valor_meta = request.POST.get('valor_meta')
        categoria_id = request.POST.get('categoria')
        imagem = request.FILES.get('imagem')

        try:
            categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
            
            Meta.objects.create(
                titulo=titulo,
                valor_meta=valor_meta,
                valor_atual=0,  # Inicializa com 0
                categoria=categoria,
                imagem=imagem
            )
            messages.success(request, 'Meta criada com sucesso!')
            return redirect('lista-metas')
        except Exception as e:
            messages.error(request, 'Erro ao criar meta. Verifique os dados e tente novamente.')
    
    return redirect('lista-metas')


def pagamentos_lista(request):
    hoje = timezone.now().date()

    # Obtenha todos os pagamentos, sem filtrar por usuário
    pagamentos_hoje = Pagamento.objects.filter(data_vencimento=hoje)
    proximos_pagamentos = Pagamento.objects.filter(
        data_vencimento__range=[hoje, hoje + timedelta(days=7)]
    ).exclude(data_vencimento=hoje)
    pagamentos_atrasados = Pagamento.objects.filter(
        data_vencimento__lt=hoje,
        status='pendente'
    )

    primeiro_dia_mes = hoje.replace(day=1)
    ultimo_dia_mes = (primeiro_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    pagamentos_mes = Pagamento.objects.filter(
        data_vencimento__range=[primeiro_dia_mes, ultimo_dia_mes]
    )

    context = {
        'pagamentos_hoje': pagamentos_hoje,
        'proximos_pagamentos': proximos_pagamentos,
        'pagamentos_atrasados': pagamentos_atrasados,
        'total_pagamentos_mes': pagamentos_mes.count(),
        'valor_total_mes': sum(p.valor for p in pagamentos_mes),
    }

    return render(request, 'financas/pagamentos.html', context)

def adicionar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            # Remova o pagamento.usuario para não exigir um usuário
            pagamento.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})

def processar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    if request.method == 'POST':
        pagamento.status = 'pago'
        pagamento.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})


def plano_de_gastos_view(request):
    hoje = timezone.now()
    mes_atual = hoje.strftime("%B %Y")

    categorias = Categoria.objects.all()
    categoria_data = [{
        'nome': cat.nome,
        'valor': float(cat.valor_total),
        'cor': cat.cor
    } for cat in categorias]

    orcamento_total = sum(cat.orcamento for cat in categorias)
    gastos_total = sum(cat.valor_total for cat in categorias)
    saldo_restante = orcamento_total - gastos_total

    despesas = DespesaPlanejada.objects.all()
    despesas_data = [{
        'id': desp.id,
        'nome': desp.nome,
        'cor': desp.cor,
        'valor_total': float(desp.valor_total),
        'valor_gasto': float(desp.valor_gasto),
        'valor_faltante': float(desp.valor_faltante),
        'percentual_gasto': desp.percentual_gasto
    } for desp in despesas]

    context = {
        'mes_atual': mes_atual,
        'categorias': categorias,
        'orcamento_total': orcamento_total,
        'gastos_total': gastos_total,
        'saldo_restante': saldo_restante,
        'despesas_planejadas': despesas,
        'categoria_data': json.dumps(categoria_data),
        'despesas_data': json.dumps(despesas_data)
    }

    return render(request, 'financas/plano_de_gastos.html', context)


def investimento_view(request):
    return render(request, 'financas/investimento.html')

def configuracoes_view(request):
    return render(request, 'financas/configuracoes.html')

