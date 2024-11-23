from django.urls import path
from . import views
from .views import baixar_tabela
from django.urls import path, include
from django.contrib.auth import views as auth_views


    
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


    path('password_reset/', views.CustomPasswordResetView.as_view(template_name='registration/recuperarSenha.html'),
        name='recuperarSenha'),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/confirmacao_email_enviado.html'),
         name='password_reset_done'),  # Adicionado para corrigir o erro

         
    path('reset/<uidb64>/<token>/',views.custom_password_reset_confirm,
        name='password_reset_confirm'),

    #CREIO QUE NAO PRECISA DISSO
    # path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/confirmacao_senha_alterada.html'),
    #      name='password_reset_complete'),

    path(
        'confirmacao-senha-alterada/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/confirmacao_senha_alterada.html'),
        name='confirmacao_senha_alterada'),
    
    
    
]