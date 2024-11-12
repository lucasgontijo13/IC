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
from django.contrib.auth import login, get_user_model
from openpyxl import Workbook
from .models import TemporaryActionModel
import plotly.graph_objs as go
import plotly.graph_objects as go
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import plotly.io as pio
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile



logger = logging.getLogger('django')


logger = logging.getLogger(__name__)

def index(request):
    # Suas variáveis e lógica atuais
    column_names = [
        'Control', 'Sub-Control', 'Ativo', 'Função de segurança', 'Título', 'Descrição',
        'NIST CSF', 'IG', 'Nome da subcategoria'
    ]
    grafico_pizza = grafico_velocimetro = grafico_linha = grafico_controle = None
    email = request.user.username
    ig_percentages = {}
    asset_type_counts = {}
    selected_date = None  # Inicializando a variável selected_date

    try:
        cliente = Cliente.objects.get(email=email)
        datas_uploads = get_unique_upload_dates(cliente)

        if request.method == 'POST':
            selected_date = request.POST.get('selected_date')  # Captura a data selecionada
            if selected_date:
                actions = ActionModel.objects.filter(upload_date=selected_date, nome=cliente.nome)

                # Gráfico de velocímetro
                sim_count = actions.filter(acao='sim').count()
                nao_count = actions.filter(acao='nao').count()
                grafico_velocimetro = create_speedometer_chart(sim_count, nao_count)

                # Calcula as porcentagens de IG e contagem de tipo de ativo
                ig_percentages = calculate_ig_percentages(actions)
                asset_type_counts = calculate_asset_type_counts(actions)

                # Gráfico de linha por controle
                grafico_controle = create_control_chart(actions)

    except Cliente.DoesNotExist:
        datas_uploads = []

    # Data com as ações, estará disponível sempre, mas os gráficos dependem da seleção da data
    data_with_actions = [
        {
            'id': item.id, 'cis_control': item.cis_control, 'cis_sub_control': item.cis_sub_control,
            'tipo_de_ativo': item.tipo_de_ativo, 'funcao_de_seguranca': item.funcao_de_seguranca,
            'titulo': item.titulo, 'descricao': item.descricao, 'nist_csf': item.nist_csf,
            'ig': item.ig, 'nome_da_subcategoria': item.nome_da_subcategoria, 'acao': ''
        } for item in framework.objects.all()
    ]

    return render(request, 'index.html', {
        'data': data_with_actions,
        'column_names': column_names,
        'datas_uploads': datas_uploads,
        'selected_date': selected_date,  # Passa a data selecionada para o template
        'grafico_velocimetro': grafico_velocimetro,
        'grafico_controle': grafico_controle,
        'ig_percentages': ig_percentages,
        'asset_type_counts': asset_type_counts,
    })








def get_unique_upload_dates(cliente):
    """Obtém datas de upload únicas associadas ao cliente no formato d/m/Y para exibição."""
    return [
        {
            'value': date.strftime('%Y-%m-%d'),       # Formato original para envio
            'display': date.strftime('%d/%m/%Y')      # Formato d/m/Y para exibição
        }
        for date in ActionModel.objects.filter(nome=cliente.nome)
                                       .values_list('upload_date', flat=True)
                                       .distinct().order_by('upload_date')
    ]

def create_speedometer_chart(sim_count, nao_count):
    """Cria o gráfico de velocímetro baseado na porcentagem de ações 'Sim'."""
    total_actions = sim_count + nao_count
    percentage = (sim_count / total_actions) * 100 if total_actions > 0 else 0
    fig_velocimetro = go.Figure(go.Indicator(
        mode="gauge+number", value=percentage,
        title={'text': "Velocímetro", 'font': {'size': 16}},
        number={'font': {'size': 28, 'color': 'blue'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "darkblue", 'thickness': 0.2},
            'bgcolor': "white", 'borderwidth': 1, 'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': "LightBlue"},
                {'range': [50, 100], 'color': "RoyalBlue"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ))
    fig_velocimetro.update_layout(
        title_text="Percentual de Ações 'Sim'", titlefont_size=16,
        margin=dict(l=35, r=35, t=30, b=10), font=dict(color='black', size=12)
    )
    return fig_velocimetro.to_html(full_html=False)

def calculate_ig_percentages(actions):
    """Calcula a porcentagem de 'Sim' para cada valor distinto de IG, ignorando 'None' e 'Não se aplica'."""
    ig_percentages = {}

    # Obtém os valores distintos de IG, excluindo os valores None
    ig_values = actions.values_list('ig', flat=True).exclude(ig=None).distinct()

    for ig in ig_values:
        # Contagem de "Sim" para o IG atual
        ig_sim_count = actions.filter(ig=ig, acao='sim').count()

        # Total de ações para o IG atual, excluindo "Não se aplica"
        ig_total = actions.filter(ig=ig).exclude(acao='nao se aplica').count()

        # Calcula a porcentagem de "Sim" para o IG atual
        ig_percentage = (ig_sim_count / ig_total) * 100 if ig_total > 0 else 0
        ig_percentages[ig] = round(ig_percentage, 2)

    return ig_percentages


def calculate_asset_type_counts(actions):
    """Calcula a contagem de 'Sim' e o total para cada tipo de ativo."""
    asset_type_counts = {}

    # Obtém os tipos de ativo distintos
    asset_types = actions.values_list('tipo_de_ativo', flat=True).distinct()

    for tipo in asset_types:
        # Conta quantos registros têm 'Sim' e o total, ignorando 'Não se aplica'
        tipo_sim_count = actions.filter(tipo_de_ativo=tipo, acao='sim').count()
        tipo_total = actions.filter(tipo_de_ativo=tipo).exclude(acao='nao se aplica').count()
        
        asset_type_counts[tipo] = {
            'sim_count': tipo_sim_count,
            'total': tipo_total
        }

    return asset_type_counts



def create_control_chart(actions):
    controls = list(range(1, 21))
    control_titles = [
        "   Inventário e Controle de<br>   Ativos de Hardware", "   Inventário e Controle de<br>   Ativos de Software",
        "   Gerenciamento contínuo<br>   de vulnerabilidades", "   Uso controlado de<br>   privilégios administrativos",
        "   Configuração segura para hardware<br>   e software em dispositivos móveis,<br>   laptops,estações de trabalho e servidores",
        "   Manutenção, Monitoramento e Análise de <br>   registros de Auditoria", "   Proteção de e-mail e<br>   navegador da Web",
        "   Defesas contra malware", "   Limitação e Controle de Portas,<br>   Protocolos e<br>   Serviços de Rede",
        "   Capacidades de<br>   recuperação de dados", "   Configuração Segura para Rede Dispositivos,<br>   como Firewalls, Roteadores e Switches",
        "   Defesa de Limites", "   Proteção de Dados", "   Acesso controlado com<br>   base na necessidade de saber",
        "   Controle de acesso<br>   sem fio", "   Monitoramento e Controle<br>   de Contas",
        "   Implementar um programa de<br>   treinamento e conscientização<br>   de segurança", "   Segurança de Software<br>   de Aplicação",
        "   Resposta e Gerenciamento<br>   de Incidentes", "   Testes de Penetração<br>   e Exercícios de Equipe Vermelha"
    ]

    # Calcula a meta para cada controle como (total de campos - campos "não se aplica")
    metas = []
    sim_counts = []
    for control in controls:
        total_campos = actions.filter(cis_control=control).count()
        nao_se_aplica = actions.filter(cis_control=control, acao='não se aplica').count()
        meta = total_campos - nao_se_aplica
        metas.append(meta)
        
        # Conta o número de "Sim" para cada controle
        sim_count = actions.filter(cis_control=control, acao='sim').count()
        sim_counts.append(sim_count)

    # Cria o gráfico de barras
    fig = go.Figure()

    # Adiciona as barras com os valores "Sim"
    fig.add_trace(go.Bar(
        x=control_titles,
        y=sim_counts,
        text=sim_counts,
        textposition='inside',
        insidetextanchor='start',  # Centraliza o texto na parte inferior da barra
        name='Aderência',
        marker=dict(color="rgb(0, 51, 102)", line=dict(color="rgb(0, 51, 102)", width=2)),
        textfont=dict(size=14, color="white")  # Aumenta a fonte e coloca a cor do texto como branca para melhor contraste
    ))

    # Adiciona a linha de meta para cada controle
    fig.add_trace(go.Scatter(
        x=control_titles,
        y=metas,
        mode='lines',
        name='Meta',
        line=dict(color='rgb(78, 177, 210)', width=2)  # Linha contínua em azul claro, sem marcadores
    ))

    # Adiciona os valores das metas acima da linha, com um pequeno deslocamento ajustando o valor de y
    fig.add_trace(go.Scatter(
        x=control_titles,
        y=[meta + 0.5 for meta in metas],  # Adiciona 2 de deslocamento aos valores das metas
        mode='text',
        text=metas,
        textposition='top center',
        showlegend=False,  # Não exibe esta entrada na legenda
        textfont=dict(size=12, color="black")
    ))

    # Configurações do layout
    fig.update_layout(
        title={
            'text': "Aderência do CIS Controls por Categoria vs Meta",
            'x': 0.5,  # Centraliza o título
            'xanchor': 'center',
            'font': {'size': 20}  # Aumenta o tamanho da fonte do título
        },
        #xaxis_title="Controle",
        #yaxis_title="Número de 'Sim'",
        yaxis=dict(range=[0, max(max(sim_counts), max(metas)) + 5]),  # Ajusta o limite do eixo y
        showlegend=True,
        barmode='group',
        bargap=0.5,  # Aumenta o espaçamento entre as barras
        template="plotly_white",
        width=1100,  # Aumenta a largura do gráfico
        height=800   # Aumenta a altura do gráfico
    )

    # Ajusta a rotação, o alinhamento e o espaçamento dos títulos no eixo X
    fig.update_xaxes(
        tickangle=90,  # Rotaciona os rótulos
        tickfont=dict(size=14),  # Aumenta a fonte dos rótulos do eixo x
        tickvals=control_titles,
        ticktext=control_titles,
        titlefont=dict(size=16),  # Aumenta o título do eixo x
        title_standoff=50,  # Ajusta o espaçamento do título do eixo X em relação aos rótulos
        
    )

    # Ajusta as margens para garantir que os rótulos não fiquem grudados
    fig.update_layout(margin=dict(l=50, r=40, t=80, b=150))  # Aumenta a margem inferior

    return fig.to_html(full_html=False)













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
                User = get_user_model()
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    password=form.cleaned_data['senha']
                )
                
                cliente = form.save(commit=False)
                cliente.user = user
                cliente.save()

                # Definir o backend explicitamente e fazer login
                backend = 'django.contrib.auth.backends.ModelBackend'
                user.backend = backend
                login(request, user, backend=backend)

                request.session['cliente_id'] = cliente.id
                logger.info('Cliente salvo com sucesso!')
                return redirect('index')  # Redireciona para a página de sucesso após o registro
            except IntegrityError:
                form.add_error(None, "Erro de integridade: possivelmente o e-mail já está em uso.")
                logger.error("Erro de integridade ao salvar cliente.")
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
                'IG': 'ig',  # Adicione o mapeamento da coluna IG
                'Nome da subcategoria': 'nome_da_subcategoria',
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
                    ig=row['IG'], # Adicione IG aqui
                    nome_da_subcategoria=row['Nome da subcategoria'],
                    
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
            today = timezone.now().date()
            #today = "2024-11-10"
            user = request.user
            nome_cliente = 'Desconhecido'

            if user.is_authenticated:
                email = user.username
                try:
                    cliente = Cliente.objects.get(email=email)
                    nome_cliente = cliente.nome
                except Cliente.DoesNotExist:
                    pass

            if request.POST.get('save') == 'temporary':
                item_id = request.POST.get('editId')
                new_action = request.POST.get(f'action_{item_id}')
                
                if item_id and new_action:
                    try:
                        framework_item = framework.objects.get(id=item_id)
                    except framework.DoesNotExist:
                        messages.error(request, 'Item do framework não encontrado.')
                        return redirect('index')

                    TemporaryActionModel.objects.update_or_create(
                        nome=nome_cliente,
                        titulo=framework_item.titulo,
                        defaults={
                            'acao': new_action,
                            'cis_control': framework_item.cis_control,
                            'cis_sub_control': framework_item.cis_sub_control,
                            'tipo_de_ativo': framework_item.tipo_de_ativo,
                            'funcao_de_seguranca': framework_item.funcao_de_seguranca,
                            'descricao': framework_item.descricao,
                            'nist_csf': framework_item.nist_csf,
                            'ig': framework_item.ig,
                            'nome_da_subcategoria': framework_item.nome_da_subcategoria,
                            'upload_date': today
                        }
                    )
                    messages.success(request, 'Ação da linha salva temporariamente.')
                else:
                    messages.error(request, 'Nenhuma linha foi selecionada para atualizar.')

            elif request.POST.get('save') == 'final':
                data_for_excel = []
                saved_count = 0

                for item in framework.objects.all():
                    action = request.POST.get(f'action_{item.id}', '')
                    action_obj, created = ActionModel.objects.update_or_create(
                        upload_date=today, nome=nome_cliente, titulo=item.titulo, cis_sub_control=item.cis_sub_control,
                        defaults={
                            'cis_control': item.cis_control,
                            'tipo_de_ativo': item.tipo_de_ativo,
                            'funcao_de_seguranca': item.funcao_de_seguranca,
                            'descricao': item.descricao,
                            'nist_csf': item.nist_csf,
                            'ig': item.ig,
                            'nome_da_subcategoria': item.nome_da_subcategoria,
                            'acao': action
                        }
                    )
                    if created:
                        saved_count += 1

                    data_for_excel.append({
                        'cis_control': item.cis_control,
                        'cis_sub_control': item.cis_sub_control,
                        'tipo_de_ativo': item.tipo_de_ativo,
                        'funcao_de_seguranca': item.funcao_de_seguranca,
                        'titulo': item.titulo,
                        'descricao': item.descricao,
                        'nist_csf': item.nist_csf,
                        'ig': item.ig,
                        'nome_da_subcategoria': item.nome_da_subcategoria,
                        'acao': action
                    })

                print(f"{saved_count} itens salvos no ActionModel.")

                df = pd.DataFrame(data_for_excel)
                df.fillna('', inplace=True)

                filename = f"{nome_cliente}_{today}.xlsx"
                file_path = f"media/{filename}"

                # Verificar se o arquivo já existe e, se sim, removê-lo
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)

                # Criar o arquivo Excel e salvar
                excel_file = BytesIO()
                df.to_excel(excel_file, index=False)
                excel_file.seek(0)
                default_storage.save(file_path, ContentFile(excel_file.read()))

                messages.success(request, 'Tabela enviada com sucesso!')

            else:
                TemporaryActionModel.objects.filter(nome=nome_cliente).delete()
                
                for item in framework.objects.all():
                    action = request.POST.get(f'action_{item.id}', '')
                    TemporaryActionModel.objects.create(
                        nome=nome_cliente,
                        cis_control=item.cis_control,
                        cis_sub_control=item.cis_sub_control,
                        tipo_de_ativo=item.tipo_de_ativo,
                        funcao_de_seguranca=item.funcao_de_seguranca,
                        titulo=item.titulo,
                        descricao=item.descricao,
                        nist_csf=item.nist_csf,
                        ig=item.ig,
                        nome_da_subcategoria=item.nome_da_subcategoria,
                        acao=action,
                        upload_date=today
                    )

                messages.success(request, 'Tabela salva temporariamente com sucesso!')

        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao atualizar a tabela: {str(e)}')

        return redirect('index')
    else:
        return redirect('index')

def download_actionModel(request):
    # Recebe parâmetros da requisição
    user_name = request.GET.get('user_name')
    submission_date_str = request.GET.get('submission_date')

    # Verifica se os parâmetros foram fornecidos
    if not user_name or not submission_date_str:
        return HttpResponse("Nome do usuário ou data não fornecidos.", status=400)

    # Converte a string de data do formato YYYY-MM-DD para um objeto de data
    try:
        submission_date = datetime.strptime(submission_date_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse("Data no formato inválido. Use o formato YYYY-MM-DD.", status=400)

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
    
    # Garantir que o nome da planilha não tenha mais de 31 caracteres
    sheet_title = f"Planilha de {user_name}"
    ws.title = sheet_title[:31]  # Truncar o título para 31 caracteres

    # Especifica os cabeçalhos das colunas
    headers = [
        "CIS Control", 
        "CIS Sub-Control", 
        "Tipo de ativo", 
        "Função de segurança", 
        "Título", 
        "Descrição",
        "NIST CSF",
        "IG",
        "Nome da subcategoria",
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
        ws.cell(row=row_num, column=8, value=registro.ig)
        ws.cell(row=row_num, column=9, value=registro.nome_da_subcategoria)
        ws.cell(row=row_num, column=10, value=registro.acao)

    # Criar a resposta HTTP com o arquivo gerado
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={user_name}_{submission_date}.xlsx'

    # Tente forçar a gravação no response
    try:
        wb.save(response)
    except Exception as e:
        print(f"Erro ao salvar o arquivo Excel: {str(e)}")
        return HttpResponse("Erro ao gerar o arquivo Excel.", status=500)

    return response

def load_temporary_table(request):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        try:
            # Obtém o email do usuário logado
            email = request.user.username
            # Encontra o cliente com base no email
            cliente = Cliente.objects.get(email=email)
            # Recupera os registros temporários para este cliente
            temp_records = TemporaryActionModel.objects.filter(nome=cliente.nome)

            # Verifica se existem registros temporários
            if not temp_records.exists():
                messages.info(request, 'Nenhum registro temporário encontrado.')
                return redirect('index')

            # Carrega os dados do framework
            data = framework.objects.all()

            # Define os nomes das colunas manualmente
            column_names = [
                'CIS Control', 'CIS Sub-Control', 'Tipo de ativo',
                'Função de segurança', 'Título', 'Descrição',
                'NIST CSF','IG','Nome da subcategoria'
            ]

            # Mapeia as ações temporárias por título
            temp_actions = {record.titulo: record.acao for record in temp_records}

            # Cria uma nova lista de dados com o campo 'acao'
            data_with_actions = []
            for item in data:
                data_with_actions.append({
                    'id': item.id,
                    'cis_control': item.cis_control,
                    'cis_sub_control': item.cis_sub_control,
                    'tipo_de_ativo': item.tipo_de_ativo,
                    'funcao_de_seguranca': item.funcao_de_seguranca,
                    'titulo': item.titulo,
                    'descricao': item.descricao,
                    'nist_csf': item.nist_csf,
                    'ig': item.ig,
                    'nome_da_subcategoria': item.nome_da_subcategoria,
                    'acao': temp_actions.get(item.titulo, ''),  # Adiciona a ação correspondente
                })

            return render(request, 'index.html', {
                'data': data_with_actions,  # Passa os dados com ações
                'column_names': column_names,
            })
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado.')
            return redirect('login')
    else:
        return redirect('login')
    




