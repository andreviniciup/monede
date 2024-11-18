# financas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_view, name='inicio'),  # Página inicial
    path('transacoes/', views.transacoes_view, name='transacoes'),  # Página de transações
    path('transacoes/nova-transacao/', views.nova_transacao, name='nova_transacao'),
    path('relatorios/', views.relatorios_view, name='relatorios'),  # Página de relatórios
    path('metas/', views.lista_metas_view, name='metas'),  # Rota para listagem de metas
    path('metas/criar/', views.criar_meta_view, name='criar-meta'), 
    path('plano_de_gastos/', views.plano_de_gastos_view, name='plano_de_gastos'),  # Página de plano de gastos
    path('pagamentos/', views.pagamentos_lista, name='pagamentos'),
    path('pagamentos/adicionar/', views.adicionar_pagamento, name='adicionar_pagamento'),
    path('pagamentos/<int:pagamento_id>/processar/', views.processar_pagamento, name='processar_pagamento'),
    path('meus-cartoes/', views.lista_cartoes, name='meus_cartoes'), 
    path('meus-cartoes/adicionar/', views.adicionar_cartao, name='adicionar_cartao'),
    path('meus-cartoes/<int:cartao_id>/pagar/', views.pagar_fatura, name='pagar_fatura'),
    path('meus-cartoes/<int:cartao_id>/transacoes/', views.transacoes_cartao, name='transacoes_cartao'),
    path('meus-cartoes/<int:cartao_id>/transacoes/adicionar/', views.adicionar_transacao, name='adicionar_transacao'),
    path('minhas-contas/', views.minhas_contas, name='minhas_contas'),
    path('minhas-contas/criar/', views.criar_conta_view, name='criar_conta'),
    path('categorias/', views.listar_categorias, name='categorias'),
    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    path('subcategorias/', views.listar_subcategorias, name='subcategorias'),
    path('subcategorias/criar/', views.criar_subcategoria, name='criar_subcategoria'),
    path('meus-limites/', views.meus_limites, name='meus_limites'),
]
