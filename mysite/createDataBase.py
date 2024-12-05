import os
from django.apps import AppConfig
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        # Conecta o sinal que será disparado após a migração
        post_migrate.connect(create_site_and_social_app, sender=self)

# Função que será chamada após as migrações
def create_site_and_social_app(sender, **kwargs):
    # Recuperar o domínio do arquivo .env
    domain = os.getenv('DOMAIN', '127.0.0.1:8000')  # Usar valor padrão se não encontrado no .env

    # Criar ou garantir que o site padrão exista
    site, created = Site.objects.get_or_create(
        domain=domain,  # Use o domínio do arquivo .env
        name='Meu Site'
    )

    # Criar ou garantir que o aplicativo social para Google seja configurado
    social_app, created = SocialApp.objects.get_or_create(
        provider='google',  # Para login com Google
        name='Google',
        client_id=settings.GOOGLE_CLIENT_ID,  # ID do cliente obtido do .env
        secret=settings.GOOGLE_SECRET,  # Segredo do cliente obtido do .env
    )

    # Associar o aplicativo social ao site
    social_app.sites.add(site)
