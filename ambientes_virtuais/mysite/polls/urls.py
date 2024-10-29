from django.urls import path
from . import views
from .views import download_actionModel
from django.urls import path, include

urlpatterns = [
    path('register/', views.registro_view, name='register'),  # Use 'registro_view' para a página de registro
    path('401/', views.error_401, name='error_401'),
    path('404/', views.error_404, name='error_404'),
    path('500/', views.error_500, name='error_500'),
    path('charts/', views.charts, name='charts'),
    path('layout-sidenav-light/', views.layout_sidenav_light, name='layout-sidenav-light'),
    path('layout-static/', views.layout_static, name='layout-static'),
    path('', views.login_view, name='login'),
    path('password/', views.password, name='password'),
    path('index/', views.index, name='index'),
    path('tables/', views.tables, name='tables'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('logout/', views.logout_view, name='logout'),
    path('update_table/', views.update_table, name='update_table'),
    path('download/', download_actionModel, name='download_actionModel'),
    path('load_temporary_table/', views.load_temporary_table, name='load_temporary_table'),

    path('accounts/', include('allauth.urls')),
]
