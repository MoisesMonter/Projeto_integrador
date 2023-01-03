from django import forms
from Users.models import User


class FormLogin(forms.Form):
    Usuario_Login= forms.CharField(max_length=100,)
    Senha_Login= forms.CharField(widget=forms.PasswordInput())

class FormUser(forms.ModelForm):
    #password
    Id_Academico = forms.IntegerField(label="Seu ID Academico")
    Senha = forms.CharField(min_length=6,max_length=50,widget=forms.PasswordInput())
    Senha2 = forms.CharField(label="Repita Senha",min_length=6,max_length=50,widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['Id_Academico','Nome','CPF','Genero','email','Senha']
        #exclude = ['']
    