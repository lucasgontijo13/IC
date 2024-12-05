import os
import django
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()  # Inicializa o Django e carrega as configurações

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def create_social_data():
    # Pega o domínio do arquivo .env
    domain = os.getenv('DOMAIN', '127.0.0.1:8000')  
    client_id = os.getenv('GOOGLE_CLIENT_ID')  # Google Client ID
    client_secret = os.getenv('GOOGLE_SECRET')  # Google Secret

    if not client_id or not client_secret:
        raise ValueError("O Google Client ID e o Secret precisam estar no arquivo .env")

    # Criar ou garantir que o site exista
    site, created = Site.objects.get_or_create(
        domain=domain,
        name="Meu Site"
    )
    print(f"Site criado: {site} - Criado: {created}")

    # Criar ou garantir que o aplicativo social para Google seja configurado
    social_app, created = SocialApp.objects.get_or_create(
        provider="google",
        name="Google",
        client_id=client_id,
        secret=client_secret,
    )
    print(f"SocialApp criado: {social_app} - Criado: {created}")

    # Associar o aplicativo social ao site
    social_app.sites.add(site)
    print("Aplicativo social adicionado ao site")

if __name__ == '__main__':
    create_social_data()
