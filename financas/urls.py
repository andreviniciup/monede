# financas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Página inicial
    path('transacoes/', views.transacoes_view, name='transacoes'),  # Página de transações
    path('relatorios/', views.relatorios_view, name='relatorios'),  # Página de relatórios
    path('metas/', views.metas_view, name='metas'),  # Página de metas financeiras
    path('perfil/', views.perfil_view, name='perfil'),  # Página de perfil e configurações
]
