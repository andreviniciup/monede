# financas/urls.py
from django.urls import path
from . import views

urlpatterns = [

    # Página inicial
    path('', views.inicio_view, name='inicio'),

    # Página de transações
    path('transacoes/', views.transacoes_view, name='transacoes'),
    path('transacoes/nova-transacao/', views.nova_transacao, name='nova_transacao'),
    path('buscar-transacoes/', views.buscar_transacoes, name='buscar-transacoes'),

    # Página de relatórios
    path('relatorios/', views.relatorios_view, name='relatorios'),

    # Rota para listagem de metas
    path('metas/', views.lista_metas_view, name='metas'), 
    path('metas/criar/', views.criar_meta_view, name='criar-meta'), 
    path('metas/atualizar-meta/<int:meta_id>/', views.atualizar_meta, name='atualizar-meta'),

    # Página de plano de gastos
    path('plano_de_gastos/', views.plano_de_gastos_view, name='plano_de_gastos'),  

    # pagina de pagamentos
    path('pagamentos/', views.pagamentos_lista, name='pagamentos'),
    path('pagamentos/adicionar/', views.adicionar_pagamento, name='adicionar_pagamento'),
    path('pagamentos/<int:pagamento_id>/processar/', views.processar_pagamento, name='processar_pagamento'),

    path('carteira/', views.carteira_views, name='carteira'),

    # Endpoints para ações específicas
    path('carteira/banco/adicionar/', views.carteira_views, name='adicionar_banco'),
    path('carteira/conta/adicionar/', views.carteira_views, name='adicionar_conta'),
    path('carteira/cartao/adicionar/', views.carteira_views, name='adicionar_cartao'),
    path('carteira/transacao/adicionar/', views.carteira_views, name='adicionar_transacao'),

    # Operações em cartões
    path('carteira/cartao/<int:cartao_id>/pagar/', views.pagar_fatura, name='pagar_fatura'),
    path('carteira/cartao/<int:cartao_id>/transacoes/', views.transacoes_cartao, name='transacoes_cartao'),

    path('categorias/', views.listar_categorias, name='categorias'),
    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    path('subcategorias/', views.listar_subcategorias, name='subcategorias'),
    path('subcategorias/criar/', views.criar_subcategoria, name='criar_subcategoria'),
    path('meus-limites/', views.meus_limites, name='meus_limites'),
]
