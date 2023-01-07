from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as login_django
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import FormUser,FormLogin,FormImagem,Formulario_part1,Formulario_part2
from Users.models import User as Usuario
from Users.models import Election,Data_Election
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm  
# Create your views here.
import datetime,re

def Logout(request):
    logout(request)
    return Login(request)


def Home(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,"home.html",{'x':False})
    else:
        try:
            
            usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
            #user_all_info=[str(x) for x in User.objects.filter(username__contains="0")] quando letra tá maiuscula
            #usuario_logado = usuario_logado.bojects.filter(Id_Academico = str(request.user))
            #return HttpResponse(f"{usuario_logado[0:2]}")
            return render(request,"home.html",{'x':True,'usuario_logado':usuario_logado})
        except:
            
            return render(request,"home.html",{'x':True})



def Register(request):
    x =str(request.user) == 'AnonymousUser'
    if str(request.user) != 'AnonymousUser':
        try:
            
            usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
            #user_all_info=[str(x) for x in User.objects.filter(username__contains="0")] quando letra tá maiuscula
            #usuario_logado = usuario_logado.bojects.filter(Id_Academico = str(request.user))
            #return HttpResponse(f"{usuario_logado[0:2]}")
            return render(request,"home.html",{'x':True,'usuario_logado':usuario_logado})
        except:
            
            return render(request,"home.html",{'x':True})
    if request.method == "GET":
        form = FormUser()
        x= str(request.user) != 'AnonymousUser'
        return render(request,'register.html',{'x': False,'form':form})
    else:

        form = FormUser(request.POST)
        username = request.POST.get('Id_Academico')
        email = request.POST.get('email') 
        password = request.POST.get('Senha')  
        if request.POST.get('Senha') == request.POST.get('Senha2'):
            if form.is_valid():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                form.save()       
                messages.success(request,"Conta Criada com Sucesso")
                return render(request,'login.html',{'x': False,'form':form})
            else: 
                messages.success(request,"Erro de Autenticação no Formulário")
                return render(request,'register.html',{'x': False,'form':form})
        else:
            messages.success(request,"Senhas não combinam")
            return render(request,'register.html',{'x': False,'form':form})


def Login(request):
    form = FormLogin(request.POST)
    if str(request.user) != 'AnonymousUser':
        return render(request,"home.html",{'x':True,"form":form})
    else:
        
        if request.method == "GET":
            return render(request,"login.html",{"form":form})
        

        if request.method == 'POST':
            username = request.POST.get('Id_Academico')
            password = request.POST.get('Senha')  
            user = authenticate(request, username = username,password = password)
            if user is not None:
                login_django(request,user)
                usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
                return render(request,"home.html",{'x':True,'usuario_logado':usuario_logado})
            return render(request,"login.html",{"form":form})


def About_us(request):
    print(request)
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,'about_us.html',{'x': False})
    else:
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        return render(request,"about_us.html",{'x':True,'usuario_logado':usuario_logado})
        

def ListaEleicoes(request):
    x= int(1)
    return render(request,'lista_eleicoes.html',{'x': x})



lista_candidatos = {}
requisições={}
def global_info(login,info,info_local,manipulacao,login_end):
    global lista_candidatos

    if info != None and info != '' and len(info) >0:
        try:
            info_local = lista_candidatos[login]
            if manipulacao == True: #caso seja necessario apagar
                info_local.remove(info)
            else:#caso contrario apenas incremente
                info_local.append(info)
                lista_candidatos[login]=info_local
        except:
            info_local.append(info)
            lista_candidatos[login]=info_local
    return lista_candidatos

def gerarumaeleicao(request):
    x =str(request.user) == 'AnonymousUser'
    if x == True:
        return render(request,"gerarumaeleicao.html",{'x':False})  

    else:

        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        lista_candidatos={}
        lista_candidatos = global_info(usuario_logado.Id_Academico,'',[],False,False)

        if request.method =='GET':
            lista_candidatos = global_info(usuario_logado.Id_Academico,request.POST.get('__Candidato__'),[],False,False)
            return render(request,"gerarumaeleicao.html",{'x':True,'form1':Formulario_part1,'form2':Formulario_part2,'usuario_logado':usuario_logado,'lista_candidatos':[],'len':0})      
        
        if Formulario_part2(request.POST).is_valid():
            candidato = request.POST.get('Gerando_Candidato')
            lista_candidatos = global_info(usuario_logado.Id_Academico,candidato,[],False,False)

            #form1 =  Formulario_part1(request.POST)
        if Formulario_part1(request.POST).is_valid(): 
            titulo = request.POST.get('Titulo')
            descricao = request.POST.get('Descricao')
            dias = datetime.timedelta(int(request.POST.get('select_day')))
            data = datetime.datetime.now()
            
            try:
                lista =lista_candidatos[usuario_logado.Id_Academico]
            except:
                lista=[]

            if len(lista) >1:
                try:##Informando o Ultimo ID de todos elementos da Eleição
                    for info in Election.objects.all():
                        id_end = info
                    id_end =  int(re.sub('[^0-9]',' ', str(id_end)))+1
                    formulario_eleicao =Election(N_Eleicao= id_end,Usuario =  usuario_logado,Titulo = titulo,Data = data,End_Data = data+dias, Descricao=descricao, Ativo=True,Disponibilizar=False)
                    formulario_eleicao.save()
                    for eleitor in lista:
                        formulario_aprofundado_eleicao= Data_Election(N_Eleicao = formulario_eleicao,Candidatos=eleitor,Votos=0)    
                        formulario_aprofundado_eleicao.save()
                    
                    
                    messages.success(request,f"{titulo} Criada com sucesso!")
                except:
                    id_end = 0
            else:
                messages.success(request,"Tenha no Mínimo mais de 1 Candidato")

            
            #formulario_eleicao =Election(N_Eleicao= id_end,Usuario =  usuario_logado,Titulo = titulo,Data = data,End_Data = data+dias, Descricao=descricao, Ativo=True,Disponibilizar=False)
            #formulario_eleicao.save()
            '''formulario_eleicao.Usuario = request.user
            formulario_eleicao.Titulo = request.POST.get('Titulo')
            formulario_eleicao.Descricao= request.POST.get('Texto')
            formulario_eleicao.Data = datetime.datetime.now()
            formulario_eleicao = GerarUmaEleicao(Usuario=  request.user,)
            print('\n\n\n',formulario_eleicao.Usuario,'\n',
                            formulario_eleicao.Titulo,'\n',
                            formulario_eleicao.Descricao,'\n',
                            formulario_eleicao.Data)
            eleicao_criada = formulario_eleicao.save()'''
        if request.method == 'POST':
            lista_candidatos = global_info(usuario_logado.Id_Academico,'',[],False,False)
            try:
                lista =lista_candidatos[usuario_logado.Id_Academico]
            except:
                lista=[]
            #print(lista)
            try:
                cont = 0
                for x in lista:
                    #print(x,end='> ')
                    if str(request.POST.get(str(x))) == "on":
                        lista_candidatos = global_info(usuario_logado.Id_Academico,x,[],True,False)
                    cont+=1

            except:
                pass
        return render(request,"gerarumaeleicao.html",{'x':True,'form1':Formulario_part1,'form2':Formulario_part2,'usuario_logado':usuario_logado,'lista_candidatos':lista,'len':len(lista)})   






























































































        
def Suport(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,'suport_site.html',{'x': False})
    else:
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        return render(request,"suport_site.html",{'x':True,'usuario_logado':usuario_logado})



def Config(request):
    if str(request.user) == 'AnonymousUser':
        return render(request,"config.html",{'x':False})
    if str(request.user) != 'AnonymousUser':
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        atual_cpf = str(usuario_logado.CPF)
        cpf_usuario=''
        for x in range (0,11,1):
            cpf_usuario += atual_cpf[x]
            if x ==2 or x == 5:
                cpf_usuario +='.'
            elif x == 8:
                cpf_usuario+='-'
        senha_usuario = ''.join(['*' for x  in range(0,len(str(usuario_logado.Senha)),1)])
        form = FormImagem(request.POST,request.FILES)
        if form.is_valid():
            '''usuario_logado.Foto.delete()'''
            usuario_logado.Foto.delete()
            usuario_logado.Foto = request.FILES['Foto']
            usuario_logado.save()
            form = FormImagem()
            print('\n\n\n',form)
        return render(request,"config.html",{'x':True,'form':form,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario),'cpf_usuario':cpf_usuario}) 
    else:
        
        print('\n\nfora')
        print('\n\nfora')
        if form.is_valid():
            form = FormImagem() 

    return render(request,"config.html",{'x':True,'form':form,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario),'cpf_usuario':cpf_usuario}) 


def configkey(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,"configkey.html",{'x':False})
    else:
        try:
            usuario_logado= Usuario.objects.get(Id_Academico = request.user)
            senha_usuario = ''.join(['*' for x  in range(0,len(str(usuario_logado.Senha)),1)])
            
            if request.method == 'POST':
                password_local=request.POST.get('password')
                password_new=request.POST.get('n_password')
                password_rep=request.POST.get('r_password')
                import os
                os.system('cls')

                if password_local == usuario_logado.Senha:
                    if str(password_new) ==str(password_rep):
                        Super_User = User.objects.get(username= str(request.user))
                        Super_User.set_password(str(request.POST['n_password']))
                        usuario_logado.Senha = request.POST['n_password']
                        Super_User.save()
                        usuario_logado.save()
                        messages.success(request,"Senha atualizada com Sucesso")
                        return render(request,"configkey.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})
                    else:
                        messages.success(request,"Novas Senhas não combinam")
                        messages.success(request,"Tente novamente.")   
                        return render(request,"configkey.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})
                else:
                    messages.success(request,"Essa não é sua senha Atual")

                    return render(request,"configkey.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})
            
            else:
                return render(request,"configkey.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})   
        except:
            return render(request,"configkey.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})    
    


def configdel(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,"config_del.html",{'x':False})
    else:
        try:
            usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
            senha_usuario = ''.join(['*' for x  in range(0,len(str(usuario_logado.Senha)),1)])
            
            if request.method == 'POST':
                password_local=request.POST.get('password')
                confirm = request.POST.get('checkbox')
                print('\n\n\n\n',confirm)
                if password_local == usuario_logado.Senha:
                    if str(confirm) == 'on':
                        messages.success(request,"Conta apagada")
                        Super_User = User.objects.get(username= str(request.user))
                        #usuario_logado.delete()
                        #Super_User.delete()
                        return render(request,'login.html')
                        
                    else:
                        messages.success(request,"Checkbox não autenticado")
                        messages.success(request,"Tente novamente.")
                else:
                    messages.success(request,"Essa não é sua senha")
                    messages.success(request,"Tente novamente.")

            return render(request,"config_del.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})    
            
        except:

            return render(request,"config_del.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})    


def plataforma(request):
    log_out = request.POST.get('logout')
    print(log_out)
    if log_out == 'LogOut':
        logout(request)
        return render(request,'login.html')
    if request.user.is_authenticated:
        return render(request,'home.html')


