from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # O email do usuário obtido pela autenticação do Google
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                # Verifica se o email já está associado a um usuário existente
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)  # Vincula o login social ao usuário existente
            except User.DoesNotExist:
                # Bloqueia o login caso o email não esteja cadastrado
                raise PermissionDenied("O login com o Google é permitido apenas para usuários já cadastrados.")
