from django.db import models
from django.utils import timezone
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Cliente(models.Model):
    cnpj = models.CharField(max_length=14, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) 

    def __str__(self):
        return self.user.username if self.user else 'Usuário não associado'  # Retorna o nome de usuário ou uma mensagem padrão

    # Propriedades para acessar o nome e o email diretamente do User
    @property
    def nome(self):
        return self.user.first_name if self.user else 'Nome não disponível'  # Verifica se 'user' existe

    @property
    def email(self):
        return self.user.email if self.user else 'Email não disponível'  # Verifica se 'user' existe





class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)





    
    

class framework(models.Model):
    cis_control = models.CharField(max_length=100)
    cis_sub_control = models.CharField(max_length=100)
    tipo_de_ativo = models.CharField(max_length=100)
    funcao_de_seguranca = models.CharField(max_length=100)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    nist_csf = models.CharField(max_length=100)
    ig = models.CharField(max_length=100, blank=True, null=True)
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
    ig = models.CharField(max_length=100, blank=True, null=True)
    nome_da_subcategoria = models.CharField(max_length=255)
    acao = models.CharField(max_length=50, blank=True, null=True)  # Coluna de ação
    upload_date = models.DateField(default=get_current_date)  # Apenas a data
  
    def __str__(self):
        return self.titulo
    
class TemporaryActionModel(models.Model):
    nome = models.CharField(max_length=255, default='Default Name')
    cis_control = models.CharField(max_length=100)
    cis_sub_control = models.CharField(max_length=100)
    tipo_de_ativo = models.CharField(max_length=100)
    funcao_de_seguranca = models.CharField(max_length=100)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    nist_csf = models.CharField(max_length=100)
    ig = models.CharField(max_length=100, blank=True, null=True)
    nome_da_subcategoria = models.CharField(max_length=255)
    acao = models.CharField(max_length=50, blank=True, null=True)
    upload_date = models.DateField(default=get_current_date)

    def __str__(self):
        return self.titulo
    

class Log(models.Model):
    # ID gerado automaticamente pelo Django
    id = models.AutoField(primary_key=True)
    
    # Cliente associado ao log (relacionamento com o modelo User)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')  # Relacionamento com o User
    
    # Data e hora do log
    data_time = models.DateTimeField(auto_now_add=True)
    
    # Descrição do log
    descricao = models.TextField()

    def __str__(self):
        return f"Log {self.id} - {self.descricao[:30]}"

    class Meta:
        db_table = 'polls_log'