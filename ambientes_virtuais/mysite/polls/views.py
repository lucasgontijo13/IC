import logging,os
from django.shortcuts import render, redirect
from .forms import ClienteForm
from django.db import IntegrityError
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .models import Cliente, Login , framework, ActionModel
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
import openpyxl
from django.http import HttpResponse
from datetime import datetime

logger = logging.getLogger('django')


logger = logging.getLogger(__name__)




def index(request):
    # Recupera todos os registros de framework
    data = framework.objects.all()

    # Define os nomes das colunas manualmente
    column_names = ['CIS Control', 'CIS Sub-Control', 'Tipo de ativo', 'Função de segurança', 'Título', 'Descrição', 'NIST CSF', 'Nome da subcategoria']

    return render(request, 'index.html', {'data': data, 'column_names': column_names})


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
            # Obtém o cliente pelo email
            cliente = Cliente.objects.get(email=email)
            # Verifica a senha
            if check_password(password, cliente.senha):
                # Autentica o usuário
                user = authenticate(username=email, password=password)
                if user is not None:
                    auth_login(request, user)
                    request.session['cliente_id'] = cliente.id

                    # Registra o login
                    Login.objects.create(
                        cliente=cliente,
                        descricao='Realizou Login'
                    )

                    return redirect('index')
                else:
                    messages.error(request, 'Email ou senha incorretos')
            else:
                messages.error(request, 'Email ou senha incorretos')
        except Cliente.DoesNotExist:
            messages.error(request, 'Email ou senha incorretos')
    
    return render(request, 'login.html')




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

            # Substituir NaN por strings vazias
            df.fillna('', inplace=True)

            # Excluir dados antigos
            framework.objects.all().delete()

            # Mapear colunas do DataFrame para campos do modelo
            column_mapping = {
                'CIS Control': 'cis_control',
                'CIS Sub-Control': 'cis_sub_control',
                'Tipo de ativo': 'tipo_de_ativo',
                'Função de segurança': 'funcao_de_seguranca',
                'Título': 'titulo',
                'Descrição': 'descricao',
                'NIST CSF': 'nist_csf',
                'Nome da subcategoria': 'nome_da_subcategoria'
            }

            # Verificar se as colunas esperadas estão presentes no DataFrame
            for col in column_mapping.keys():
                if col not in df.columns:
                    messages.error(request, f'Coluna {col} não encontrada no arquivo Excel.')
                    return redirect('index')

            # Salvar os dados no banco de dados
            for index, row in df.iterrows():
                framework.objects.create(
                    cis_control=row['CIS Control'],
                    cis_sub_control=row['CIS Sub-Control'],
                    tipo_de_ativo=row['Tipo de ativo'],
                    funcao_de_seguranca=row['Função de segurança'],
                    titulo=row['Título'],
                    descricao=row['Descrição'],
                    nist_csf=row['NIST CSF'],
                    nome_da_subcategoria=row['Nome da subcategoria']
                )
            
            # Excluir o arquivo após o upload
            os.remove(fs.path(filename))
            messages.success(request, 'Arquivo enviado com sucesso!')
        
        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {str(e)}')
            return redirect('index')
        
        return redirect('index')
    
    return redirect('index')

def update_table(request):
    if request.method == 'POST':
        try:
            # Variável de data para teste
            #test_date = timezone.datetime(2024, 8, 14).date()
            #today = test_date

            #Pegando a data do dia
            today = timezone.now().date()

            # Obtém o e-mail do usuário logado
            user = request.user
            if user.is_authenticated:
                email = user.username  # Assumindo que o username é o e-mail
                try:
                    # Encontre o cliente usando o e-mail
                    cliente = Cliente.objects.get(email=email)
                    nome_cliente = cliente.nome
                except Cliente.DoesNotExist:
                    nome_cliente = 'Desconhecido'  # Nome padrão se o cliente não for encontrado
            else:
                nome_cliente = 'Desconhecido'

            # Verifica se já existe um registro para o cliente e a data atual
            existing_records = ActionModel.objects.filter(upload_date=today, nome=nome_cliente)

            # Exclui todos os registros existentes para o cliente e o dia atual
            if existing_records.exists():
                existing_records.delete()

            # Cria novos registros com base nos itens do framework
            for item in framework.objects.all():
                action = request.POST.get(f'action_{item.id}')
                if action:
                    ActionModel.objects.create(
                        nome=nome_cliente,  # Nome do cliente logado
                        cis_control=item.cis_control,
                        cis_sub_control=item.cis_sub_control,
                        tipo_de_ativo=item.tipo_de_ativo,
                        funcao_de_seguranca=item.funcao_de_seguranca,
                        titulo=item.titulo,
                        descricao=item.descricao,
                        nist_csf=item.nist_csf,
                        nome_da_subcategoria=item.nome_da_subcategoria,
                        acao=action,
                        upload_date=today  # Usa a data de teste
                    )
            messages.success(request, 'Tabela atualizada e salva com sucesso!')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao atualizar a tabela: {str(e)}')
        return redirect('index')
    else:
        return redirect('index')

def download_actionModel(request):
    # Recebe parâmetros da requisição
    user_name = request.GET.get('user_name')
    submission_date_str = request.GET.get('submission_date')

    # Adiciona logs para depuração
    print(f"Data recebida: {submission_date_str}")

    # Verifica se os parâmetros foram fornecidos
    if not user_name or not submission_date_str:
        return HttpResponse("Nome do usuário ou data não fornecidos.", status=400)

    # Converte a string de data do formato YYYY-MM-DD para um objeto de data
    try:
        submission_date = datetime.strptime(submission_date_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse("Data no formato inválido. Use o formato YYYY-MM-DD.", status=400)

    # Adiciona logs para depuração
    print(f"Procurando registros para usuário: {user_name} e data: {submission_date}")

    # Busca os registros que correspondem ao nome e data fornecidos
    registros = ActionModel.objects.filter(
        nome=user_name,
        upload_date=submission_date  # Comparando a data completa, sem hora
    )

    if not registros.exists():
        return HttpResponse("Nenhum registro encontrado para os critérios fornecidos.", status=404)

    # Cria um novo workbook e sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Planilha de {user_name}"

    # Especifica os cabeçalhos das colunas
    headers = [
        "CIS Control", 
        "CIS Sub-Control", 
        "Tipo de ativo", 
        "Função de segurança", 
        "Título", 
        "Descrição",
        "NIST CSF",
        "Nome da subcategoria"
        "Ação"
    ]

    # Insere os cabeçalhos na primeira linha
    for col_num, header in enumerate(headers, 1):
        ws.cell(row=1, column=col_num, value=header)

    # Preenche a planilha com os dados do banco de dados
    for row_num, registro in enumerate(registros, 2):
        ws.cell(row=row_num, column=1, value=registro.cis_control)
        ws.cell(row=row_num, column=2, value=registro.cis_sub_control)
        ws.cell(row=row_num, column=3, value=registro.tipo_de_ativo)
        ws.cell(row=row_num, column=4, value=registro.funcao_de_seguranca)
        ws.cell(row=row_num, column=5, value=registro.titulo)
        ws.cell(row=row_num, column=6, value=registro.descricao)
        ws.cell(row=row_num, column=7, value=registro.nist_csf)
        ws.cell(row=row_num, column=8, value=registro.nome_da_subcategoria)
        ws.cell(row=row_num, column=9, value=registro.acao)

    # Cria o arquivo em memória
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={user_name}_{submission_date}.xlsx'

    # Salva a planilha no response
    wb.save(response)
    return response
