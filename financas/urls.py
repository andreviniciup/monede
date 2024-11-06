# financas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_view, name='inicio'),  # Página inicial
    path('transacoes/', views.transacoes_view, name='transacoes'),  # Página de transações
    path('relatorios/', views.relatorios_view, name='relatorios'),  # Página de relatórios
    path('metas/', views.metas_view, name='metas'),  # Página de metas financeiras
    path('pagamentos/', views.pagamentos_view, name='pagamentos'),  # Página de pagamentos
    path('plano_de_gastos/', views.plano_de_gastos_view, name='plano_de_gastos'),  # Página de plano de gastos
    path('investimento/', views.investimento_view, name='investimento'),  # Página de investimento
    path('configuracoes/', views.configuracoes_view, name='configuracoes'),  # Página de investimento
]
