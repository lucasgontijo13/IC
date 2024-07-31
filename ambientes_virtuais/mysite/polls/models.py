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
    
    

class MyModel(models.Model):
    column1 = models.CharField(max_length=100)
    column2 = models.IntegerField()
    column3 = models.DateField()

    def __str__(self):
        return self.column1