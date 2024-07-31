# mysite/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('polls.urls')),  # Inclui as URLs do aplicativo polls
    path('admin/', admin.site.urls),
    # Outras URLs do seu projeto aqui, se houver
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
