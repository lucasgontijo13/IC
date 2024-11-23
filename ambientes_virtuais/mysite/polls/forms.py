from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Cliente
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

User = get_user_model()

class ClienteForm(forms.ModelForm):
    primeiro_nome = forms.CharField(max_length=50, label='Primeiro Nome')
    sobrenome = forms.CharField(max_length=50, label='Sobrenome')
    email = forms.EmailField(label='Email')
    senha = forms.CharField(widget=forms.PasswordInput, label='Senha')
    confirmar_senha = forms.CharField(widget=forms.PasswordInput, label='Confirme sua senha')

    class Meta:
        model = Cliente
        fields = ['cnpj', 'primeiro_nome', 'sobrenome', 'email', 'senha', 'confirmar_senha']

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if not cnpj.isdigit() or len(cnpj) != 14:
            raise ValidationError("O CNPJ deve ter exatamente 14 dígitos numéricos.")
        return cnpj

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', "As senhas não coincidem.")  # Associa o erro ao campo 'confirmar_senha'
        return cleaned_data

    def save(self, commit=True):
        cliente = super().save(commit=False)
        senha = self.cleaned_data.get('senha')
        email = self.cleaned_data.get('email')
        primeiro_nome = self.cleaned_data.get('primeiro_nome')
        sobrenome = self.cleaned_data.get('sobrenome')

        if commit:
            # Criar o usuário do Django
            user = User.objects.create_user(
                username=email,  # O username será o email
                password=senha,
                first_name=primeiro_nome,
                last_name=sobrenome,
                email=email
            )
            cliente.user = user
            cliente.save()
        return cliente




class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Autentica o usuário com email e senha
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Email ou senha inválidos.")
        return cleaned_data
