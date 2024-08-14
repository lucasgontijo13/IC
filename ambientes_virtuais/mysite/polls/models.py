from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True, null=False, default='default@example.com')
    cnpj = models.CharField(max_length=14, unique=True, default='00000000000000')
    senha = models.CharField(max_length=128, null=True)  # Limitar senha para 8 caracteres
    data_cadastro = models.DateTimeField(blank=True, null=True)  # Adicionando o campo last_login
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    

    def __str__(self):
        return self.nome 
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Login(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relacionamento com Cliente
    data_time = models.DateTimeField(default=timezone.now)  # Adiciona a data e hora de criação
    descricao = models.CharField(max_length=45, default='Entrou')

    def __str__(self):
        return f'{self.cliente.nome} - {self.descricao}'
    
    

class framework(models.Model):
    cis_control = models.CharField(max_length=100)
    cis_sub_control = models.CharField(max_length=100)
    tipo_de_ativo = models.CharField(max_length=100)
    funcao_de_seguranca = models.CharField(max_length=100)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    nist_csf = models.CharField(max_length=100)
    nome_da_subcategoria = models.CharField(max_length=255)
    upload_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.titulo
    
def get_current_date():
    return timezone.now().date()

class ActionModel(models.Model):
    nome = models.CharField(max_length=255, default='Default Name')
    cis_control = models.CharField(max_length=100)
    cis_sub_control = models.CharField(max_length=100)
    tipo_de_ativo = models.CharField(max_length=100)
    funcao_de_seguranca = models.CharField(max_length=100)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    nist_csf = models.CharField(max_length=100)
    nome_da_subcategoria = models.CharField(max_length=255)
    acao = models.CharField(max_length=50, blank=True, null=True)  # Coluna de ação
    upload_date = models.DateField(default=get_current_date)  # Apenas a data
  
    def __str__(self):
        return self.titulo
    
