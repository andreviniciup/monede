from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from .models import Transacao, Categoria, DespesaPlanejada, Pagamento, Meta, Limites , Subcategoria, Cartao, Conta, Banco, Logo
from .forms import TransacaoForm, PagamentoForm, CategoriaForm, SubcategoriaForm, CartaoForm, TransacaoCartaoForm, ContaForm, BancoForm
import json
import joblib
import requests
from datetime import datetime, timedelta


modelo_ml = joblib.load('ml_model.pkl')


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


def obter_logo_via_api(marca_nome):
    """
    Tenta obter o logo de uma marca utilizando múltiplas fontes.
    """
    fontes = [buscar_logo_brandfetch, buscar_logo_clearbit]  
    
    for fonte in fontes:
        logo = fonte(marca_nome)  # Tenta buscar o logo com cada fonte
        if logo:  # Se encontrar um logo, retorna
            return logo
    
    # Retorna logo padrão se nenhuma fonte encontrar
    print(f"Logo não encontrado para {marca_nome}. Usando logo padrão.")
    logo, _ = Logo.objects.get_or_create(
        nome="Padrão",
        defaults={"imagem": "path/para/logo-padrao.png"}
    )
    return logo

def buscar_logo_clearbit(marca_nome):
    """
    Busca o logo no Clearbit.
    """
    dominio = marca_nome.lower() + ".com"
    url_logo = f"https://logo.clearbit.com/{dominio}"
    
    try:
        response = requests.get(url_logo)
        response.raise_for_status()
        
        logo, criado = Logo.objects.get_or_create(nome=marca_nome)
        if criado:
            logo.imagem.save(f"{marca_nome}.png", ContentFile(response.content), save=True)
            print(f"Logo para {marca_nome} adicionado com sucesso via Clearbit.")
        
        return logo
    
    except requests.exceptions.RequestException as e:
        print(f"Erro no Clearbit para {marca_nome}: {e}")
        return None

def buscar_logo_brandfetch(marca_nome):
    """
    Busca o logo em formato SVG no Brandfetch.
    """
    api_key = "ZcieYBn6Hg1UT9emBlVg3iyCYqTBttnMe7HmU+xQmQ8="  
    url = f"https://api.brandfetch.io/v2/brands/{marca_nome.lower()}.com"
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        # Procurar por um logo em formato SVG
        logos = data.get("logos", [])
        svg_logo_url = next((logo["url"] for logo in logos if logo["type"] == "svg"), None)
        
        if svg_logo_url:
            response_logo = requests.get(svg_logo_url)
            response_logo.raise_for_status()
            
            logo, criado = Logo.objects.get_or_create(nome=marca_nome)
            if criado:
                logo.imagem.save(f"{marca_nome}.svg", ContentFile(response_logo.content), save=True)
                print(f"Logo SVG para {marca_nome} adicionado com sucesso via Brandfetch.")
            
            return logo
        
        print(f"Logo SVG para {marca_nome} não encontrado no Brandfetch.")
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"Erro no Brandfetch para {marca_nome}: {e}")
        return None


def transacoes_view(request):
    transacoes = Transacao.objects.all()

    # Verifica se ambos os parâmetros de data foram passados pela URL
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    # Filtra as transações apenas quando ambos os campos de data foram selecionados
    if data_inicial and data_final:
        try:
            data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
            data_final = datetime.strptime(data_final, '%Y-%m-%d')

            # Aplica o filtro de data somente se ambas as datas forem válidas
            if data_inicial <= data_final:
                transacoes = transacoes.filter(data__gte=data_inicial, data__lte=data_final)
            else:
                messages.error(request, 'A data inicial não pode ser maior que a data final.')
        except ValueError:
            messages.error(request, 'Uma ou ambas as datas estão no formato inválido.')

    # Processamento do formulário de nova transação
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)

            # Usar o modelo de ML para prever a marca com base no título da transação
            marca_prevista = modelo_ml.predict([transacao.titulo])[0]
            
            # Buscar o logo no banco de dados ou via API se não existir
            logo = Logo.objects.filter(nome__iexact=marca_prevista).first()
            if not logo:
                logo = obter_logo_via_api(marca_prevista)

            # Associar o logo previsto à transação
            if logo:
                transacao.logo = logo

            transacao.save()
            messages.success(request, 'Transação adicionada com sucesso.')
            return redirect('transacoes')
        else:
            messages.error(request, 'Erro ao adicionar transação. Verifique os dados e tente novamente.')
    else:
        form = TransacaoForm()

    # Renderiza a página com as transações e o formulário
    return render(request, 'financas/transacoes.html', {
        'transacoes': transacoes,
        'form': form,
        'data_inicial': data_inicial,
        'data_final': data_final,
    })


def nova_transacao(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        valor = request.POST.get('valor')
        categoria_id = request.POST.get('categoria')
        conta_id = request.POST.get('conta')
        tipo = request.POST.get('tipo')  # Verifique se há um campo 'tipo' no formulário
        
        # Verifique se data automática está ativada
        data_automatica = request.POST.get('data_automatica')
        data = request.POST.get('data') if not data_automatica else timezone.now()
        
        try:
            # Buscar categoria e conta associadas
            categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
            
            # Prever marca com o modelo de ML
            marca_prevista = modelo_ml.predict([titulo])[0]
            
            # Buscar ou obter logo via API
            logo = Logo.objects.filter(nome__iexact=marca_prevista).first()
            if not logo:
                logo = obter_logo_via_api(marca_prevista)

            # Criar a transação
            Transacao.objects.create(
                titulo=titulo,
                valor=valor,
                data=data,
                categoria=categoria,
                tipo=tipo,
                logo=logo
            )
            
            messages.success(request, 'Transação criada com sucesso!')
            return redirect('transacoes')
        except Exception as e:
            print(f"Erro: {e}")
            messages.error(request, f'Erro ao criar transação: {e}')
    
    # Caso GET ou erro no POST, redirecionar para o formulário
    categorias = Categoria.objects.all()
    contas = Conta.objects.all()
    return render(request, 'financas/transacoes.html', {'categorias': categorias, 'contas': contas})


def buscar_transacoes(request):
    try:
        query = request.GET.get('q', '')  # Captura o termo da pesquisa
        resultados = Transacao.objects.none()  # Inicia com um queryset vazio
        colunas = [
            ('titulo', 'titulo__icontains'),
            ('valor', 'valor__icontains'),
            ('data', 'data__icontains'),
            ('categoria', 'categoria__nome__icontains'),
            ('tipo', 'tipo__icontains'),
        ]

        # Testa as colunas em sequência
        for nome_coluna, filtro_coluna in colunas:
            if not resultados.exists():  # Continua apenas se não houver resultados
                print(f"Buscando em {nome_coluna} com '{query}'...")
                resultados = Transacao.objects.filter(**{filtro_coluna: query})
                if resultados.exists():
                    print(f"Resultados encontrados em {nome_coluna}: {resultados}")

        # Adiciona filtro para forma de pagamento (Cartao ou Conta)
        if not resultados.exists():
            forma_pagamento_content_types = ContentType.objects.get_for_models(Cartao, Conta).values()
            for content_type in forma_pagamento_content_types:
                resultados = Transacao.objects.filter(
                    forma_pagamento_type=content_type,
                    forma_pagamento_id__in=content_type.model_class().objects.filter(nome__icontains=query).values_list('id', flat=True)
                )
                if resultados.exists():
                    print(f"Resultados encontrados em forma de pagamento: {resultados}")
                    break

        # Serializar resultados para JSON
        dados = []
        for transacao in resultados:
            forma_pagamento_nome = ''
            if transacao.forma_pagamento:
                forma_pagamento_nome = transacao.forma_pagamento.nome

            logo_url = ''
            if transacao.logo:
                logo_url = transacao.logo.imagem.url

            dados.append({
                'titulo': transacao.titulo,
                'valor': float(transacao.valor),
                'data': transacao.data.strftime('%Y-%m-%d %H:%M:%S') if transacao.data else '',
                'categoria': transacao.categoria.nome if transacao.categoria else '',
                'tipo': transacao.tipo,
                'forma_pagamento': forma_pagamento_nome,
                'logo_url': logo_url,
                'id': transacao.id
            })

        print(f"Resultados finais: {dados}")  # Exibe os resultados encontrados
        return JsonResponse({'transacoes': dados, 'quantidade': resultados.count()})

    except Exception as e:
        # Registrar erro para debug
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

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

@csrf_exempt  # Para testes locais; em produção, use o middleware CSRF
def atualizar_meta(request, meta_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Decodifica o JSON recebido
            valor_meta = data.get('valor_meta')  # Obtém o campo 'valor_meta'

            print("Valor recebido no backend:", valor_meta)


            if valor_meta is None:  # Validação
                return JsonResponse({'error': 'O campo valor_meta é obrigatório.'}, status=400)

            meta = Meta.objects.get(id=meta_id)
            meta.valor_atual += float(valor_meta)  # Atualiza o valor atual
            meta.save()

            return JsonResponse({'success': True, 'nova_meta': meta.valor_atual})
        except Meta.DoesNotExist:
            return JsonResponse({'error': 'Meta não encontrada.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido.'}, status=405)

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


def carteira_views(request):
    contas = Conta.objects.all()  
    bancos = Banco.objects.all()  
    cartoes = Cartao.objects.all()
    
    # Formulários
    banco_form = BancoForm()
    conta_form = ContaForm()
    cartao_form = CartaoForm()
    transacao_form = TransacaoCartaoForm()

    # Tratamento de diferentes formulários
    if request.method == 'POST':
        if 'adicionar_banco' in request.POST:  # Identifica qual formulário foi enviado
            banco_form = BancoForm(request.POST, request.FILES)
            if banco_form.is_valid():
                banco_form.save()
                messages.success(request, 'Banco adicionado com sucesso!')
                return redirect('meus_cartoes')

        elif 'adicionar_conta' in request.POST:
            conta_form = ContaForm(request.POST)
            if conta_form.is_valid():
                conta = conta_form.save(commit=False)
                conta.usuario = request.user
                conta.save()
                messages.success(request, 'Conta criada com sucesso!')
                return redirect('meus_cartoes')

        elif 'adicionar_cartao' in request.POST:
            cartao_form = CartaoForm(request.POST)
            if cartao_form.is_valid():
                cartao = cartao_form.save(commit=False)
                cartao.usuario = request.user
                cartao.save()
                messages.success(request, 'Cartão adicionado com sucesso!')
                return redirect('meus_cartoes')

        elif 'adicionar_transacao' in request.POST:
            transacao_form = TransacaoCartaoForm(request.POST)
            if transacao_form.is_valid():
                transacao = transacao_form.save(commit=False)
                transacao.cartao_id = request.POST.get('cartao_id')  # Recebe o ID do cartão do formulário
                transacao.save()
                messages.success(request, 'Transação adicionada com sucesso!')
                return redirect('meus_cartoes')

    context = {
        'contas': contas,
        'bancos': bancos,
        'cartoes': cartoes,
        'banco_form': banco_form,
        'conta_form': conta_form,
        'cartao_form': cartao_form,
        'transacao_form': transacao_form
    }

    return render(request, 'financas/meus_cartoes.html', context)


def pagar_fatura(request, cartao_id):
    """View para realizar o pagamento de uma fatura."""
    cartao = get_object_or_404(Cartao, id=cartao_id)  # Remove a verificação de usuário.

    if request.method == 'POST':
        # Lógica de pagamento
        cartao.saldo -= cartao.valor_fatura  # Exemplo: subtraindo o valor da fatura do saldo
        cartao.valor_fatura = 0  # Zera a fatura após o pagamento
        cartao.save()

        messages.success(request, 'Fatura paga com sucesso!')
        return JsonResponse({'status': 'success', 'message': 'Fatura paga com sucesso!'})

    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)


def transacoes_cartao(request, cartao_id):
    """View para listar e gerenciar transações de um cartão."""
    cartao = get_object_or_404(Cartao, id=cartao_id)  # Remove a verificação de usuário.
    transacoes = cartao.transacoes_cartao.all()  # `related_name` do relacionamento entre cartão e transações.

    # Filtros de data
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    if data_inicial and data_final:
        transacoes = transacoes.filter(data__range=[data_inicial, data_final])

    transacao_form = TransacaoCartaoForm()

    if request.method == 'POST':
        transacao_form = TransacaoCartaoForm(request.POST)
        if transacao_form.is_valid():
            transacao = transacao_form.save(commit=False)
            transacao.cartao = cartao
            transacao.save()

            messages.success(request, 'Transação adicionada com sucesso!')
            return redirect('transacoes_cartao', cartao_id=cartao.id)
        else:
            messages.error(request, 'Erro ao adicionar transação. Verifique os dados.')

    context = {
        'cartao': cartao,
        'transacoes': transacoes,
        'transacao_form': transacao_form,
    }

    return render(request, 'financas/transacoes_cartao.html', context)


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
