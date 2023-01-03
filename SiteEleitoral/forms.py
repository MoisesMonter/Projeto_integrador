from django import forms
from Users.models import User


class Senha_padrao(forms.Form):
    Senha = forms.CharField(min_length=6,max_length=50,widget=forms.PasswordInput())

class FormUser(forms.ModelForm):
    #password
    Senha=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['Id_Academico','Nome','CPF','Genero','email','Senha',]
    