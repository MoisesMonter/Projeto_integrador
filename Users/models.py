from distutils.command.upload import upload
from django.db import models
from django import forms
# Create your models here.
from django import forms
Sexo_Choices = (
    ('M','Masculino'),
    ('F','Feminino'),
)

class User(models.Model):
    Id_Academico = models.CharField(max_length=15,unique=True,primary_key=True)
    Nome = models.CharField(max_length=50,null = False)
    CPF = models.CharField(max_length=11,unique=True,null=False)
    Genero =models.CharField(max_length=1,choices=Sexo_Choices)
    email = models.EmailField(blank=True,null=True)
    Senha = models.CharField(max_length=50)#+str(Id_Academico)+'/'
    Foto=models.ImageField('Imagem do perfil',upload_to="",default=None)
    
    def __str__(self):
        return self.Id_Academico





class Election(models.Model):
    N_Eleicao = models.IntegerField(unique=True,primary_key=True)
    Usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    Titulo = models.CharField(max_length=30, null = False)
    Data = models.DateField()
    Descricao = models.CharField(max_length=150,null = True)
    Ativo = models.BooleanField()
    Disponibilizar= models.BooleanField()

    def __str__(self) -> str:
        return super().__str__()

class Activity_Report(models.Model):
    Usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    ID_REPORT = models.IntegerField(unique=True,null=False)
    Titulo = models.CharField(max_length=50)
    Balao  = models.CharField(max_length=300,null =False)
    Imagem = models.ImageField(upload_to="BD_User_Report/")

    def __str__(self) -> str:
        return super().__str__()

class Activity_User(models.Model):
    Usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    Participacao = models.ForeignKey(Election,on_delete=models.CASCADE)
    Report = models.ForeignKey(Activity_Report,on_delete=models.CASCADE)
    Horario = models.DateField()

    Disponibilizar= models.BooleanField()

    def __str__(self) -> str:
        return super().__str__()

class Data_Election(models.Model):
    N_Eleicao = models.ForeignKey(Election,on_delete=models.CASCADE)
    Candidatos = models.CharField(max_length=50,unique=True)
    Votos = models.IntegerField(null = False)

    def __str__(self) -> str:
        return super().__str__()

class Interaction_User(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    N_Eleicao = models.ForeignKey(Election,on_delete=models.CASCADE)
    Data = models.DateField()

    def __str__(self) -> str:
        return super().__str__()