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
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('meus-cartoes/', views.meus_cartoes, name='meus_cartoes'),
    path('minhas-contas/', views.minhas_contas, name='minhas_contas'),
    path('categorias/', views.categorias, name='categorias'),
    path('subcategorias/', views.subcategorias, name='subcategorias'),
    path('meus-limites/', views.meus_limites, name='meus_limites'),
]
