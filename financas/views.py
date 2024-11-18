from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.http import JsonResponse
from .models import Transacao, Categoria, DespesaPlanejada, Pagamento, Meta, Limites , Subcategoria, Cartao
from .forms import TransacaoForm, PagamentoForm, CategoriaForm, SubcategoriaForm, CartaoForm, TransacaoCartaoForm
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

def nova_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transação adicionada com sucesso.')
            return redirect('transacoes')
        else:
            messages.error(request, 'Erro ao adicionar transação. Verifique os dados e tente novamente.')
    else:
        form = TransacaoForm()

    return render(request, 'financas/nova_transacao.html', {'form': form})


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
    
    return redirect('metas')


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


def minhas_contas(request):
    return render(request, 'financas/minhas_contas.html')

def meus_cartoes(request):
    return render(request, 'financas/meus_cartoes.html')


def lista_cartoes(request):
    cartoes = Cartao.objects.all()
    form = CartaoForm()
    return render(request, 'financas/lista_cartoes.html', {
        'cartoes': cartoes,
        'form': form
    })


def adicionar_cartao(request):
    if request.method == 'POST':
        form = CartaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cartoes')
    return redirect('lista_cartoes')


def pagar_fatura(request, cartao_id):
    if request.method == 'POST':
        cartao = Cartao.objects.get(id=cartao_id)
        cartao.status = 'FECHADA'
        cartao.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def transacoesCartao(request, cartao_id):
    cartao = Cartao.objects.get(id=cartao_id)
    transacoes = cartao.transacao_set.all()
    
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    
    if data_inicial and data_final:
        transacoes = transacoes.filter(data__range=[data_inicial, data_final])
    
    form = TransacaoCartaoForm()
    
    return render(request, 'cartoes/transacoes.html', {
        'cartao': cartao,
        'transacoes': transacoes,
        'form': form
    })

def adicionar_transacao(request, cartao_id):
    if request.method == 'POST':
        form = TransacaoCartaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.cartao_id = cartao_id
            transacao.save()
            return redirect('transacoes', cartao_id=cartao_id)
    return redirect('transacoes', cartao_id=cartao_id)

def meus_limites(request):
    return render(request, 'financas/meus_limites.html')

def novo_limite(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        titulo = request.POST.get('titulo')
        valor = request.POST.get('valor')
        recorrencia = request.POST.get('recorrencia')
        data_inicio = request.POST.get('data_inicio')
        
        
        categoria = Categoria.objects.get(id=categoria_id)
        
        
        Limites.objects.create(
            categoria=categoria,
            titulo=titulo,
            valor=valor,
            recorrencia=recorrencia,
            data_inicio=data_inicio
        )
        
        return redirect('dashboard')
    
    
    categories = Categoria.objects.all().order_by('name')
    return render(request, 'limits/novo_limite.html', {'categories': categories})

# API view to get categories (optional - for dynamic loading)
def get_categories(request):
    categories = Categoria.objects.all().order_by('name')
    return JsonResponse({
        'categories': list(categories.values('id', 'name', 'icon'))
    })


def listar_categorias(request):
    categorias_usuario = Categoria.objects.filter(padrao=False)
    categorias_padrao = Categoria.objects.filter(padrao=True)
    formulario = CategoriaForm()
    
    contexto = {
        'categorias_usuario': categorias_usuario,
        'categorias_padrao': categorias_padrao,
        'formulario': formulario,
    }
    return render(request, 'financas/categorias.html', contexto)

def criar_categoria(request):
    if request.method == 'POST':
        formulario = CategoriaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('categorias')
        else:
            messages.error(request, "Erro ao criar a categoria. Verifique os dados do formulário.")
    return redirect('categorias')



# API view to get subcategories (optional - for dynamic loading)
def get_subcategories(request):
    subcategories = Subcategoria.objects.all().order_by('name')
    return JsonResponse({
        'subcategories': list(subcategories.values('id', 'name', 'icon'))
    })


def listar_subcategorias(request):
    subcategorias_usuario = Subcategoria.objects.filter(padrao=False)
    subcategorias_padrao = Subcategoria.objects.filter(padrao=True)
    formulario = SubcategoriaForm()
    
    contexto = {
        'subcategorias_usuario': subcategorias_usuario,
        'subcategorias_padrao': subcategorias_padrao,
        'formulario': formulario,
    }
    return render(request, 'financas/subcategorias.html', contexto)

def criar_subcategoria(request):
    if request.method == 'POST':
        formulario = SubcategoriaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('subcategorias')
        else:
            messages.error(request, "Erro ao criar a subcategoria. Verifique os dados do formulário.")
    return redirect('subcategorias')
