from django.urls import path
from . import views
from .views import baixar_tabela
from django.urls import path, include


urlpatterns = [
    path('register/', views.registro_view, name='register'),  
    path('', views.login_view, name='login'),
    path('index/', views.index, name='index'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('logout/', views.logout_view, name='logout'),
    path('atualiza_tabela/', views.atualiza_tabela, name='atualiza_tabela'),
    path('download/', baixar_tabela, name='baixar_tabela'),
    path('carrega_tabela_temporaria/', views.carrega_tabela_temporaria, name='carrega_tabela_temporaria'),
    path('cria_grafico_velocimetro/', views.cria_grafico_velocimetro, name='cria_grafico_velocimetro'),
    path('get_unique_upload_dates/', views.data_consulta_grafico, name='data_consulta_grafico'),

    path('accounts/', include('allauth.urls')),
    
]