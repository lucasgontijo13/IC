from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.contrib.auth.models import User
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from .models import Cliente,Log

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # O email do usuário obtido pela autenticação do Google
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                # Verifica se o email já está associado a um usuário existente
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)  # Vincula o login social ao usuário existente

                # Garantir que o cliente_id seja atribuído à sessão após login
                cliente = Cliente.objects.get(user=user)
                request.session['cliente_id'] = cliente.id  # Armazena o cliente_id na sessão

                # Registrar o login no modelo Log
                Log.objects.create(
                    cliente=user,
                    descricao=f'O cliente {user.first_name} {user.last_name} realizou login via Google.'
                )

            except User.DoesNotExist:
                # Bloqueia o login caso o email não esteja cadastrado
                messages.error(request, "Essa conta Google não está cadastrada. Por favor, registre-se.")
                raise ImmediateHttpResponse(redirect('register'))
        else:
            # Se o fluxo for interrompido (ex: clicar em cancelar), redirecionar para login
            messages.warning(request, "Login cancelado. Por favor, tente novamente.")
            raise ImmediateHttpResponse(redirect('/login'))




