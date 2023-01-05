from django import forms
from Users.models import User


class FormLogin(forms.Form):
    Id_Academico =forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'placeholder':'Enter numbers Only'}))
    Senha = forms.CharField(min_length=6,max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'off','placeholder':'******'}))

class FormUser(forms.ModelForm):
    #password
    Id_Academico =forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'placeholder':'Enter numbers Only'}))
    Nome =  forms.CharField(label='Nome completo',required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'on', 'placeholder':'Thaysa Fernandes'}))
    CPF =forms.CharField(label='Seu CPF',min_length=11,required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'placeholder':'Enter numbers Only '}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','autocomplete':'on','placeholder':'EmailUsuario@outlook.com'}))
    Senha = forms.CharField(min_length=6,max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'off','placeholder':'******'}))
    Senha2 = forms.CharField(label="Repita Senha",min_length=6,max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'off','placeholder':'******'}))

    class Meta:
        model = User
        fields = ['Id_Academico','Nome','CPF','Genero','email','Senha']
        #exclude = ['']

    
class FormImagem(forms.ModelForm):
    #Senha = forms.CharField(min_length=6,max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'off','placeholder':'******'}))
    
    class Meta:
        model = User
        fields = ['Foto']
        
        widgets = {
                'Foto': forms.FileInput(attrs= {'style':'color:#2e303300;','class':'form-control', 'required': False,})

            }