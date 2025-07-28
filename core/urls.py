from django.urls import path
from . import views
from .views import check_po_exists

urlpatterns = [
    path('', views.painel_tv, name='painel_tv'),
    path('painel/lancamentos/', views.lancamento_list, name='lancamento_list'),
    path('painel/lancamentos/novo/', views.lancamento_create, name='lancamento_create'),
    path('painel/lancamentos/<int:pk>/editar/', views.lancamento_update, name='lancamento_update'),
    path('painel/lancamentos/<int:pk>/excluir/', views.lancamento_delete, name='lancamento_delete'),

    # Nova rota para a tela de Configurações
    path('configuracoes/', views.configuracoes, name='configuracoes'),


    path('exportar-processos/', views.exportar_processos, name='exportar_processos'),

    path('check-po-exists/', check_po_exists, name='check_po_exists'),
]
