from django import forms
from Users.models import User,Data_Election


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


class Select_day(forms.Form):#formulario para finalizar cadastro de eleições
    select_day = forms.ChoiceField(label='Selecione quantos dias', choices=(('1',1),('2',2),('3',3),('4',4),(5,'5'),(6,'6'),('7',7),('8',8),('9',9),('10',10),('11',11),('12',12),('13',13),('14',14),('15',15)))
    #Form_Form = forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'on', 'placeholder':'Titulo da Eleição', 'value':"Doe",'style':'display:None;'}))

class Formulario_part1(forms.Form):
    Titulo = forms.CharField(label='Titulo',max_length=30,required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'on', 'placeholder':'Titulo da Eleição'}))
    Descricao = forms.CharField(label="Descrição",max_length=300,widget=forms.Textarea(attrs={"rows":"5",'placeholder':'Resuma em 300 linhas',"data-ls-module":"charCounter"}))
    #Data = forms.DateField(label='Data',widget=forms.DateInput(format='%d-%m-%Y',attrs={'type':'date',}),input_formats=('%d-%m-%Y'))

class Formulario_part2(forms.Form):
    Gerando_Candidato = forms.CharField(label='Gerar Candidato',max_length=30,required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'on', 'placeholder':'Nome do Candidato'}))



class Formularios_Para_Votar(forms.Form):
    Form1 = forms.CharField(label='Titulo',max_length=30,required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'on', 'placeholder':'Titulo da Eleição', 'value':'1','style':'display:None;'}))
    Form2 = forms.CharField(label='Titulo',max_length=30,required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'on', 'placeholder':'Titulo da Eleição', 'value':'2','style':'display:None;'}))




