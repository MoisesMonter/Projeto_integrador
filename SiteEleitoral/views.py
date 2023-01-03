from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import FormUser,FormLogin
from Users.models import User as Usuario
from django.urls import reverse_lazy
# Create your views here.

def login_logout(request):
    pass


def Home(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        pass
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
    if str(request.user) != 'AnonymousUser':
        print(request.user)
        return render(request,"home.html")
    if request.method == "GET":
        return render(request,"login.html")
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username =username,password=password)
        print("user = " + str(user)) #always returns None
        if user: # se não for falso
            login_django(request,user)
            return render(request,'home.html')
        else:
            return HttpResponse(f"{user}")
            return render(request,'login.html')

def About_us(request):
    x= int(1)
    return render(request,'about_us.html',{'x': x})

def ListaEleicoes(request):
    x= int(1)
    return render(request,'lista_eleicoes.html',{'x': x})



def Suport(request):
    x= int(1)
    return render(request,'suport_site.html',{'x': x})



def Config(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,"config.html",{'x':False})
    else:
        try:
            
            usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
            #user_all_info=[str(x) for x in User.objects.filter(username__contains="0")] quando letra tá maiuscula
            #usuario_logado = usuario_logado.bojects.filter(Id_Academico = str(request.user))
            #return HttpResponse(f"{usuario_logado[0:2]}")
            return render(request,"config.html",{'x':True,'usuario_logado':usuario_logado})
        except:
            
            return render(request,"config.html",{'x':True})




def plataforma(request):
    log_out = request.POST.get('logout')
    print(log_out)
    if log_out == 'LogOut':
        logout(request)
        return render(request,'login.html')
    if request.user.is_authenticated:
        return render(request,'home.html')



