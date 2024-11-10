# financas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_view, name='inicio'),  # Página inicial
    path('transacoes/', views.transacoes_view, name='transacoes'),  # Página de transações
    path('relatorios/', views.relatorios_view, name='relatorios'),  # Página de relatórios
    path('metas/', views.lista_metas_view, name='metas'),  # Rota para listagem de metas
    path('metas/criar/', views.criar_meta_view, name='criar-meta'), 
    path('plano_de_gastos/', views.plano_de_gastos_view, name='plano_de_gastos'),  # Página de plano de gastos
    path('investimento/', views.investimento_view, name='investimento'),  # Página de investimento
    path('configuracoes/', views.configuracoes_view, name='configuracoes'),  # Página de investimento
    path('pagamentos/', views.pagamentos_lista, name='pagamentos'),
    path('pagamentos/adicionar/', views.adicionar_pagamento, name='adicionar_pagamento'),
    path('pagamentos/<int:pagamento_id>/processar/', views.processar_pagamento, name='processar_pagamento'),
]
