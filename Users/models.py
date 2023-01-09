from distutils.command.upload import upload
from django.db import models,migrations
from django.db.models import signals
from django.template.defaultfilters import slugify
from django import forms
import django.core.files.storage

#pip install django-stdimage
# or
#pipenv install django-stdimage
from stdimage import StdImageField, JPEGField

# Create your models here.
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
    Senha = models.CharField(max_length=50)
    Foto= models.ImageField('Imagem do perfil', upload_to='profile', default=None)
    #''' imagem = JPEGField('Foto de Perfil',upload_to='profile',variations={ 'thumbnail': (200, 200)},default="profile",)'''
    def __str__(self):
        return self.Id_Academico


class Election(models.Model):
    N_Eleicao = models.IntegerField(unique=True,primary_key=True,auto_created=True)
    Usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    Titulo = models.CharField(max_length=30, null = False)
    Data = models.DateField(null= True)
    End_Data = models.DateField(null= True)
    Descricao = models.CharField(max_length=150,null = True)
    Ativo = models.BooleanField()
    Disponibilizar= models.BooleanField()

    def __str__(self):
        return  str(self.N_Eleicao)

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
    N_Eleicao = models.ForeignKey(Election,on_delete=models.CASCADE,unique=False)
    Candidatos = models.CharField(max_length=50,unique=True)
    N_Candidato = models.IntegerField()
    Votos = models.IntegerField(null = False)

    def __str__(self):
        return str(self.N_Eleicao)

class Interaction_User(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    N_Eleicao = models.ForeignKey(Election,on_delete=models.CASCADE)
    Data = models.DateField()

    def __str__(self) -> str:
        return super().__str__()