import logging,os
from django.shortcuts import render, redirect
from .forms import ClienteForm
from django.db import IntegrityError
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .models import Cliente, Login , MyModel
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout


logger = logging.getLogger('django')


logger = logging.getLogger(__name__)

def logout_view(request):
    cliente_id = request.session.get('cliente_id')
    if cliente_id:
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            # Registrar o logout
            Login.objects.create(
                cliente=cliente,
                descricao='Realizou Logout'
            )
        except Cliente.DoesNotExist:
            logger.error(f'Cliente com ID {cliente_id} não encontrado.')
    
    django_logout(request)
    return redirect('login')



def upload_excel(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, 'Nenhum arquivo selecionado.')
            return redirect('index')
        
        excel_file = request.FILES['file']
        if not excel_file:
            messages.error(request, 'Nenhum arquivo selecionado.')
            return redirect('index')

        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        uploaded_file_url = fs.url(filename)

        try:
            # Ler o arquivo Excel
            df = pd.read_excel(fs.path(filename))

            # Excluir dados antigos
            MyModel.objects.all().delete()

            # Salvar os dados no banco de dados
            for index, row in df.iterrows():
                MyModel.objects.create(
                    column1=row.get('Column1', ''),
                    column2=row.get('Column2', 0),
                    column3=row.get('Column3', pd.NaT)
                )

            # Excluir o arquivo após o upload
            os.remove(fs.path(filename))

            messages.success(request, 'Arquivo enviado com sucesso!')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {str(e)}')

    return redirect('index')  # Redireciona para a página index

def registro_view(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    password=form.cleaned_data['senha']
                )
                cliente = form.save(commit=False)
                cliente.user = user
                cliente.save()
                
                login(request, user)
                request.session['cliente_id'] = cliente.id
                
                logger.info('Cliente salvo com sucesso!')
                return redirect('index')  # Redireciona para a página de sucesso após o registro
            except IntegrityError:
                # As mensagens de erro já foram adicionadas ao formulário no método save()
                pass
        else:
            logger.error('Formulário inválido: %s', form.errors)
    else:
        form = ClienteForm()
    
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            cliente = Cliente.objects.get(email=email)
            if check_password(password, cliente.senha):
                request.session['cliente_id'] = cliente.id
                
                Login.objects.create(
                    cliente=cliente,
                    descricao='Realizou Login'
                )
                
                return redirect('index')
            else:
                messages.error(request, 'Email ou senha incorretos')
        except Cliente.DoesNotExist:
            messages.error(request, 'Email ou senha incorretos')
    
    return render(request, 'login.html')


def index(request):
    # Recupera todos os registros de MyModel
    data = MyModel.objects.all()
    return render(request, 'index.html', {'data': data})

def error_401(request):
    return render(request, '401.html')

def error_404(request, exception):
    return render(request, '404.html')

def error_500(request):
    return render(request, '500.html')

def charts(request):
    return render(request, 'charts.html')

def layout_sidenav_light(request):
    return render(request, 'layout-sidenav-light.html')

def layout_static(request):
    return render(request, 'layout-static.html')

def password(request):
    return render(request, 'password.html')

def register(request):
    return render(request, 'register.html')

def tables(request):
    return render(request, 'tables.html')
