from django import forms
from django.db import IntegrityError
from .models import Cliente, Login
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class ClienteForm(forms.ModelForm):
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'}),
        label='Confirme sua senha'
    )

    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'cnpj', 'senha']
        widgets = {
            'senha': forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}),
        }

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        if senha:
            if len(senha) != 8:
                raise forms.ValidationError("A senha deve ter exatamente 8 caracteres.")
        return senha

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj and len(cnpj) != 14:
            raise forms.ValidationError("O CNPJ deve ter exatamente 14 dígitos.")
        return cnpj

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', 'As senhas não coincidem.')

        return cleaned_data

    def save(self, commit=True):
        cliente = super().save(commit=False)
        senha = self.cleaned_data.get('senha')
        
        if senha:
            cliente.senha = make_password(senha)
        
        if commit:
            if not cliente.data_cadastro:
                cliente.data_cadastro = timezone.now()  # Adiciona a data de cadastro
            cliente.save()
            # Criar uma nova entrada de Login
            Login.objects.create(
                cliente=cliente,
                data_time=timezone.now(),
                descricao='Realizou Cadastro'
            )
        
        return cliente
    
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

